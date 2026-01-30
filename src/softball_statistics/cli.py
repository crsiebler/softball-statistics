"""
Command-line interface for softball statistics.
"""

import sys
import argparse
from pathlib import Path
from softball_statistics.repository.sqlite import SQLiteRepository
from softball_statistics.parsers.csv_parser import parse_csv_file, create_database_objects, CSVParseError
from softball_statistics.exporters.excel_exporter import export_to_excel, ExcelExportError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Softball Statistics Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  softball-stats --file fray-cyclones-winter-01.csv --output stats.xlsx
  softball-stats --list-leagues
  softball-stats --list-teams --league "fray"
        """
    )

    parser.add_argument(
        '--file',
        type=str,
        help='CSV file to process (with format: league-team-season-game.csv)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='stats.xlsx',
        help='Output Excel file path (default: stats.xlsx)'
    )

    parser.add_argument(
        '--list-leagues',
        action='store_true',
        help='List all leagues in the database'
    )

    parser.add_argument(
        '--list-teams',
        action='store_true',
        help='List teams (requires --league)'
    )

    parser.add_argument(
        '--league',
        type=str,
        help='League name for --list-teams'
    )

    args = parser.parse_args()

    # Initialize repository
    repo = SQLiteRepository('softball_stats.db')

    try:
        if args.list_leagues:
            _list_leagues(repo)
        elif args.list_teams:
            if not args.league:
                print("Error: --league is required with --list-teams")
                sys.exit(1)
            _list_teams(repo, args.league)
        elif args.file:
            _process_file(repo, args.file, args.output)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def _list_leagues(repo: SQLiteRepository):
    """List all leagues."""
    leagues = repo.list_leagues()
    if not leagues:
        print("No leagues found.")
        return

    print("Leagues:")
    for league in leagues:
        print(f"  - {league.name} ({league.season})")


def _list_teams(repo: SQLiteRepository, league_name: str):
    """List teams in a league."""
    # First find the league
    leagues = repo.list_leagues()
    league = next((l for l in leagues if l.name == league_name), None)
    if not league or league.id is None:
        print(f"League '{league_name}' not found.")
        return

    teams = repo.list_teams_by_league(league.id)
    if not teams:
        print(f"No teams found in league '{league_name}'.")
        return

    print(f"Teams in {league_name}:")
    for team in teams:
        print(f"  - {team.name}")


def _process_file(repo: SQLiteRepository, file_path: str, output_path: str):
    """Process a CSV file."""
    try:
        # Parse the CSV file
        print(f"Parsing {file_path}...")
        parsed_data = parse_csv_file(file_path)

        # Create database objects
        print("Creating database objects...")
        objects = create_database_objects(parsed_data)

        # Check if game already exists
        metadata = parsed_data['metadata']
        if repo.game_exists(metadata['league'], metadata['team'], metadata['season'], metadata['game']):
            response = input(f"Game {metadata['league']}-{metadata['team']}-{metadata['season']}-{metadata['game']} already exists. Replace? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Operation cancelled.")
                return

            # Delete existing data
            print("Removing existing game data...")
            repo.delete_game_data(metadata['league'], metadata['team'], metadata['season'], metadata['game'])

        # Save to repository
        print("Saving to database...")
        repo.save_game_data(objects)

        # Save parsing warnings
        warnings = parsed_data.get('warnings', [])
        if warnings:
            print(f"Saving {len(warnings)} parsing warning(s)...")
            repo.save_parsing_warnings(warnings)

        # Export to Excel
        print(f"Exporting to {output_path}...")

        # Get all stats for export
        # Find the team and get player stats
        leagues = repo.list_leagues()
        league = next((l for l in leagues if l.name == metadata['league'] and l.season == metadata['season']), None)
        team_stats = {}
        if league and league.id:
            teams = repo.list_teams_by_league(league.id)
            team = next((t for t in teams if t.name == metadata['team']), None)
            if team and team.id:
                # Get all players for this team and their stats
                players_data = []
                with repo._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT id, name FROM players WHERE team_id = ?', (team.id,))
                    players = cursor.fetchall()

                for player_id, player_name in players:
                    stats = repo.get_player_stats(player_id)
                    if stats:
                        # Create a modified PlayerStats with name
                        player_stats_dict = {
                            'player_id': player_id,
                            'player_name': player_name,
                            'at_bats': stats.at_bats,
                            'hits': stats.hits,
                            'singles': stats.singles,
                            'doubles': stats.doubles,
                            'triples': stats.triples,
                            'home_runs': stats.home_runs,
                            'rbis': stats.rbis,
                            'runs_scored': stats.runs_scored,
                            'batting_average': stats.batting_average,
                            'on_base_percentage': stats.on_base_percentage,
                            'slugging_percentage': stats.slugging_percentage,
                            'ops': stats.ops
                        }
                        players_data.append(player_stats_dict)

                team_stats = {
                    metadata['team']: {
                        'players': players_data,
                        'games_played': 1  # Simplified
                    }
                }

        stats_data = {
            'league_name': metadata['league'],
            'season': metadata['season'],
            'team_stats': team_stats
        }

        export_to_excel(stats_data, output_path)
        print(f"Success! Statistics exported to {output_path}")

        # Display parsing warnings if any
        if warnings:
            print(f"\n⚠️  Parsing Warnings ({len(warnings)}):")
            for warning in warnings:
                location = ""
                if warning['row_num'] and warning['col_num'] and warning['filename']:
                    location = f" (row {warning['row_num']}, column {warning['col_num']} in {warning['filename']})"
                elif warning['filename']:
                    location = f" (in {warning['filename']})"
                
                print(f"  - Player '{warning['player_name']}': {warning['assumption']}{location}")
                print(f"    Original: '{warning['original_attempt']}'")

    except (CSVParseError, ExcelExportError) as e:
        print(f"Processing failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()