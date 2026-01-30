"""
Excel exporter for softball statistics.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from softball_statistics.interfaces import QueryRepository
from softball_statistics.models import PlayerStats

logger = logging.getLogger(__name__)


class ExcelExportError(Exception):
    """Raised when Excel export fails."""


class ExcelExporter:
    """Excel exporter implementing Exporter interface."""

    def __init__(self, query_repo: QueryRepository):
        self.query_repo = query_repo

    def export(self, data: Dict[str, Any], output_path: str) -> None:
        """Export data to Excel."""
        export_to_excel(data, output_path, self.query_repo)


def export_to_excel(
    stats_data: Dict[str, Any],
    output_path: str,
    query_repo: Optional[QueryRepository] = None,
) -> None:
    """
    Export softball statistics to an Excel file with multiple sheets.

    Args:
        stats_data: Dictionary containing league/team stats and metadata
        output_path: Path to save the Excel file

    Raises:
        ExcelExportError: If export fails
    """
    try:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            # Create legend sheet first
            _create_legend_sheet(writer)

            # Always create league summary sheet
            _create_league_summary_sheet(stats_data, writer)

            # Create comprehensive player summary sheet (if query_repo available)
            if query_repo:
                _create_player_summary_sheet(query_repo, writer)

            # Team sheets
            for team_name, team_stats in stats_data.get("team_stats", {}).items():
                _create_team_sheet(team_name, team_stats, writer)

            # Individual player sheets (if requested)
            if stats_data.get("include_player_details", False):
                for team_name, team_stats in stats_data.get("team_stats", {}).items():
                    for player_stats in team_stats.get("players", []):
                        _create_player_sheet(player_stats, writer)

        logger.info(f"Successfully exported statistics to {output_path}")

    except Exception as e:
        raise ExcelExportError(f"Failed to export to Excel: {e}")


def _create_league_summary_sheet(
    stats_data: Dict[str, Any], writer: pd.ExcelWriter
) -> None:
    """Create the league summary sheet."""
    stats_data.get("league_name", "Unknown League")
    stats_data.get("season", "Unknown Season")

    summary_data = []
    for team_name, team_stats in stats_data.get("team_stats", {}).items():
        # Calculate team totals for PA, BB, SF (removed from display but kept for potential future use)
        players = team_stats.get("players", [])
        sum(p.get("plate_appearances", 0) for p in players)
        sum(p.get("walks", 0) for p in players)
        sum(p.get("sacrifice_flies", 0) for p in players)

        summary_data.append(
            {
                "Team": team_name,
                "Games Played": team_stats.get("games_played", 0),
                "Total Players": len(players),
                "Team BA": f"{team_stats.get('team_batting_average', 0):.3f}",
                "Team OBP": f"{team_stats.get('team_on_base_percentage', 0):.3f}",
                "Team SLG": f"{team_stats.get('team_slugging_percentage', 0):.3f}",
                "Team OPS": f"{team_stats.get('team_ops', 0):.3f}",
            }
        )

    # Always create at least a summary sheet, even if empty
    if not summary_data:
        summary_data = [
            {
                "Team": "No teams found",
                "Games Played": 0,
                "Total Players": 0,
                "Team BA": "0.000",
                "Team OBP": "0.000",
                "Team SLG": "0.000",
                "Team OPS": "0.000",
            }
        ]

    df = pd.DataFrame(summary_data)
    df.to_excel(writer, sheet_name="League Summary", index=False)

    # Format the sheet
    worksheet = writer.sheets["League Summary"]
    worksheet.column_dimensions["A"].width = 20  # Team
    worksheet.column_dimensions["B"].width = 15  # Games Played
    worksheet.column_dimensions["C"].width = 16  # Total Players
    worksheet.column_dimensions["D"].width = 12  # Team BA
    worksheet.column_dimensions["E"].width = 12  # Team OBP
    worksheet.column_dimensions["F"].width = 12  # Team SLG
    worksheet.column_dimensions["G"].width = 12  # Team OPS


def _create_team_sheet(
    team_name: str, team_stats: Dict[str, Any], writer: pd.ExcelWriter
) -> None:
    """Create a sheet for team statistics."""
    player_data = []

    for player_info in team_stats.get("players", []):
        player_data.append(
            {
                "Player": player_info.get(
                    "player_name", f"Player {player_info.get('player_id', 'Unknown')}"
                ),
                "PA": player_info.get("plate_appearances", 0),
                "AB": player_info.get("at_bats", 0),
                "H": player_info.get("hits", 0),
                "1B": player_info.get("singles", 0),
                "2B": player_info.get("doubles", 0),
                "3B": player_info.get("triples", 0),
                "HR": player_info.get("home_runs", 0),
                "BB": player_info.get("walks", 0),
                "SF": player_info.get("sacrifice_flies", 0),
                "RBI": player_info.get("rbis", 0),
                "R": player_info.get("runs_scored", 0),
                "BA": f"{player_info.get('batting_average', 0):.3f}",
                "OBP": f"{player_info.get('on_base_percentage', 0):.3f}",
                "SLG": f"{player_info.get('slugging_percentage', 0):.3f}",
                "OPS": f"{player_info.get('ops', 0):.3f}",
            }
        )

    if player_data:
        df = pd.DataFrame(player_data)
        # Sort by Player name alphabetically (case-insensitive)
        df = df.sort_values("Player", key=lambda x: x.str.lower(), ascending=True)

        # Add team totals row
        if player_data:
            totals_row = {
                "Player": "TEAM TOTALS",
                "PA": sum(player["PA"] for player in player_data),
                "AB": sum(player["AB"] for player in player_data),
                "H": sum(player["H"] for player in player_data),
                "1B": sum(player["1B"] for player in player_data),
                "2B": sum(player["2B"] for player in player_data),
                "3B": sum(player["3B"] for player in player_data),
                "HR": sum(player["HR"] for player in player_data),
                "BB": sum(player["BB"] for player in player_data),
                "SF": sum(player["SF"] for player in player_data),
                "RBI": sum(player["RBI"] for player in player_data),
                "R": sum(player["R"] for player in player_data),
                "BA": f"{team_stats.get('team_batting_average', 0):.3f}",
                "OBP": f"{team_stats.get('team_on_base_percentage', 0):.3f}",
                "SLG": f"{team_stats.get('team_slugging_percentage', 0):.3f}",
                "OPS": f"{team_stats.get('team_ops', 0):.3f}",
            }
            # Append totals row to DataFrame
            totals_df = pd.DataFrame([totals_row])
            df = pd.concat([df, totals_df], ignore_index=True)

        sheet_name = f"{team_name[:25]}"  # Excel sheet names limited to 31 chars
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Format the sheet
        worksheet = writer.sheets[sheet_name]
        worksheet.column_dimensions["A"].width = 20  # Player name
        worksheet.column_dimensions["B"].width = 8  # PA
        worksheet.column_dimensions["C"].width = 8  # AB
        worksheet.column_dimensions["D"].width = 8  # H
        worksheet.column_dimensions["E"].width = 8  # 1B
        worksheet.column_dimensions["F"].width = 8  # 2B
        worksheet.column_dimensions["G"].width = 8  # 3B
        worksheet.column_dimensions["H"].width = 8  # HR
        worksheet.column_dimensions["I"].width = 8  # BB
        worksheet.column_dimensions["J"].width = 8  # SF
        worksheet.column_dimensions["K"].width = 8  # RBI
        worksheet.column_dimensions["L"].width = 8  # R
        worksheet.column_dimensions["M"].width = 10  # BA
        worksheet.column_dimensions["N"].width = 10  # OBP
        worksheet.column_dimensions["O"].width = 10  # SLG
        worksheet.column_dimensions["P"].width = 10  # OPS


def _create_legend_sheet(writer: pd.ExcelWriter) -> None:
    """Create a legend sheet explaining abbreviations and formulas."""
    legend_data = [
        {
            "Abbreviation": "PA",
            "Full Name": "Plate Appearances",
            "Formula": "AB + BB + SF",
        },
        {
            "Abbreviation": "AB",
            "Full Name": "At Bats",
            "Formula": "Total attempts - BB - SF",
        },
        {"Abbreviation": "H", "Full Name": "Hits", "Formula": "Total bases gained > 0"},
        {"Abbreviation": "1B", "Full Name": "Singles", "Formula": "Hits with 1 base"},
        {"Abbreviation": "2B", "Full Name": "Doubles", "Formula": "Hits with 2 bases"},
        {"Abbreviation": "3B", "Full Name": "Triples", "Formula": "Hits with 3 bases"},
        {
            "Abbreviation": "HR",
            "Full Name": "Home Runs",
            "Formula": "Hits with 4 bases",
        },
        {
            "Abbreviation": "BB",
            "Full Name": "Walks/Bases on Balls",
            "Formula": "Outcome = 'BB'",
        },
        {
            "Abbreviation": "SF",
            "Full Name": "Sacrifice Flies",
            "Formula": "Fly ball outcomes with RBI",
        },
        {
            "Abbreviation": "RBI",
            "Full Name": "Runs Batted In",
            "Formula": "Runs scored on play",
        },
        {
            "Abbreviation": "R",
            "Full Name": "Runs Scored",
            "Formula": "Runs scored by batter",
        },
        {"Abbreviation": "BA", "Full Name": "Batting Average", "Formula": "H / AB"},
        {
            "Abbreviation": "OBP",
            "Full Name": "On-Base Percentage",
            "Formula": "(H + BB + HBP + SF) / (AB + BB + HBP + SF)",
        },
        {
            "Abbreviation": "SLG",
            "Full Name": "Slugging Percentage",
            "Formula": "Total Bases / AB",
        },
        {
            "Abbreviation": "OPS",
            "Full Name": "On-Base Plus Slugging",
            "Formula": "OBP + SLG",
        },
    ]

    df = pd.DataFrame(legend_data)
    df.to_excel(writer, sheet_name="Legend", index=False)

    # Format the sheet
    worksheet = writer.sheets["Legend"]
    worksheet.column_dimensions["A"].width = 15  # Abbreviation
    worksheet.column_dimensions["B"].width = 25  # Full Name
    worksheet.column_dimensions["C"].width = 40  # Formula


def _create_player_summary_sheet(
    query_repo: QueryRepository, writer: pd.ExcelWriter
) -> None:
    """Create comprehensive player summary sheet with all players from all leagues/seasons."""
    from softball_statistics.repository.sqlite import SQLiteQueryRepository

    player_data = []

    if isinstance(query_repo, SQLiteQueryRepository):
        with query_repo._get_connection() as conn:
            cursor = conn.cursor()
            # Get all players with their team names
            cursor.execute(
                """
                SELECT p.id, p.name, t.name as team_name
                FROM players p
                JOIN teams t ON p.team_id = t.id
                ORDER BY p.name
            """
            )

            players = cursor.fetchall()

            for player_id, player_name, team_name in players:
                stats = query_repo.get_player_stats(player_id)
                if stats:
                    player_data.append(
                        {
                            "Player": player_name,
                            "Team": team_name,
                            "PA": stats.plate_appearances,
                            "AB": stats.at_bats,
                            "H": stats.hits,
                            "1B": stats.singles,
                            "2B": stats.doubles,
                            "3B": stats.triples,
                            "HR": stats.home_runs,
                            "BB": stats.walks,
                            "SF": stats.sacrifice_flies,
                            "RBI": stats.rbis,
                            "R": stats.runs_scored,
                            "BA": f"{stats.batting_average:.3f}",
                            "OBP": f"{stats.on_base_percentage:.3f}",
                            "SLG": f"{stats.slugging_percentage:.3f}",
                            "OPS": f"{stats.ops:.3f}",
                        }
                    )

    if player_data:
        df = pd.DataFrame(player_data)
        # Sort alphabetically by player name (case-insensitive)
        df = df.sort_values("Player", key=lambda x: x.str.lower(), ascending=True)

        df.to_excel(writer, sheet_name="Player Summary", index=False)

        # Format the sheet
        worksheet = writer.sheets["Player Summary"]
        worksheet.column_dimensions["A"].width = 20  # Player name
        worksheet.column_dimensions["B"].width = 20  # Team name
        worksheet.column_dimensions["C"].width = 8  # PA
        worksheet.column_dimensions["D"].width = 8  # AB
        worksheet.column_dimensions["E"].width = 8  # H
        worksheet.column_dimensions["F"].width = 8  # 1B
        worksheet.column_dimensions["G"].width = 8  # 2B
        worksheet.column_dimensions["H"].width = 8  # 3B
        worksheet.column_dimensions["I"].width = 8  # HR
        worksheet.column_dimensions["J"].width = 8  # BB
        worksheet.column_dimensions["K"].width = 8  # SF
        worksheet.column_dimensions["L"].width = 8  # RBI
        worksheet.column_dimensions["M"].width = 8  # R
        worksheet.column_dimensions["N"].width = 10  # BA
        worksheet.column_dimensions["O"].width = 10  # OBP
        worksheet.column_dimensions["P"].width = 10  # SLG
        worksheet.column_dimensions["Q"].width = 10  # OPS


def _create_player_sheet(player_stats: PlayerStats, writer: pd.ExcelWriter) -> None:
    """Create detailed player sheet (optional)."""
    # For now, just create a simple summary
    # In the future, this could include game-by-game breakdowns
    data = [
        {
            "Statistic": "Games Played",
            "Value": "TBD",  # Would need to track this in PlayerStats
        },
        {"Statistic": "At Bats", "Value": player_stats.at_bats},
        {"Statistic": "Hits", "Value": player_stats.hits},
        {
            "Statistic": "Batting Average",
            "Value": f"{player_stats.batting_average:.3f}",
        },
        {
            "Statistic": "On Base Percentage",
            "Value": f"{player_stats.on_base_percentage:.3f}",
        },
        {
            "Statistic": "Slugging Percentage",
            "Value": f"{player_stats.slugging_percentage:.3f}",
        },
        {"Statistic": "OPS", "Value": f"{player_stats.ops:.3f}"},
    ]

    df = pd.DataFrame(data)
    sheet_name = f"Player_{player_stats.player_id}_detail"
    df.to_excel(writer, sheet_name=sheet_name, index=False)
