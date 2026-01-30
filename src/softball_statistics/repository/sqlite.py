"""
SQLite implementation of the repository interface.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from datetime import date
from softball_statistics.models import League, Team, Player, Week, Game, AtBatAttempt, PlayerStats
from softball_statistics.repository.base import Repository
from softball_statistics.calculators.stats_calculator import calculate_batting_stats


class SQLiteRepository(Repository):
    """SQLite implementation of the repository."""

    def __init__(self, db_path: str):
        """Initialize repository with database path."""
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Create all database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS leagues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    season TEXT NOT NULL,
                    UNIQUE(name, season)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    league_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY (league_id) REFERENCES leagues(id),
                    UNIQUE(league_id, name)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY (team_id) REFERENCES teams(id),
                    UNIQUE(team_id, name)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS weeks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    league_id INTEGER NOT NULL,
                    week_number INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    FOREIGN KEY (league_id) REFERENCES leagues(id),
                    UNIQUE(league_id, week_number)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_id INTEGER NOT NULL,
                    team_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    opponent_team_id INTEGER,
                    FOREIGN KEY (week_id) REFERENCES weeks(id),
                    FOREIGN KEY (team_id) REFERENCES teams(id),
                    FOREIGN KEY (opponent_team_id) REFERENCES teams(id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS at_bats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL,
                    outcome TEXT NOT NULL,
                    bases INTEGER DEFAULT 0,
                    rbis INTEGER DEFAULT 0,
                    runs_scored INTEGER DEFAULT 0,
                    FOREIGN KEY (player_id) REFERENCES players(id),
                    FOREIGN KEY (game_id) REFERENCES games(id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS parsing_warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    row_num INTEGER,
                    col_num INTEGER,
                    filename TEXT,
                    original_attempt TEXT NOT NULL,
                    assumption TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def _get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def save_league(self, league: League) -> int:
        """Save a league and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if league.id is None:
                cursor.execute(
                    'INSERT INTO leagues (name, season) VALUES (?, ?)',
                    (league.name, league.season)
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE leagues SET name = ?, season = ? WHERE id = ?',
                    (league.name, league.season, league.id)
                )
                return league.id

    def get_league(self, league_id: int) -> Optional[League]:
        """Get a league by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, season FROM leagues WHERE id = ?', (league_id,))
            row = cursor.fetchone()
            if row:
                return League(id=row[0], name=row[1], season=row[2])
            return None

    def list_leagues(self) -> List[League]:
        """List all leagues."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, season FROM leagues ORDER BY name')
            return [League(id=row[0], name=row[1], season=row[2]) for row in cursor.fetchall()]

    def save_team(self, team: Team) -> int:
        """Save a team and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if team.id is None:
                cursor.execute(
                    'INSERT INTO teams (league_id, name) VALUES (?, ?)',
                    (team.league_id, team.name)
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE teams SET league_id = ?, name = ? WHERE id = ?',
                    (team.league_id, team.name, team.id)
                )
                return team.id

    def get_team(self, team_id: int) -> Optional[Team]:
        """Get a team by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, league_id, name FROM teams WHERE id = ?', (team_id,))
            row = cursor.fetchone()
            if row:
                return Team(id=row[0], league_id=row[1], name=row[2])
            return None

    def list_teams_by_league(self, league_id: int) -> List[Team]:
        """List all teams in a league."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, league_id, name FROM teams WHERE league_id = ? ORDER BY name', (league_id,))
            return [Team(id=row[0], league_id=row[1], name=row[2]) for row in cursor.fetchall()]

    def save_player(self, player: Player) -> int:
        """Save a player and return their ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if player.id is None:
                cursor.execute(
                    'INSERT INTO players (team_id, name) VALUES (?, ?)',
                    (player.team_id, player.name)
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE players SET team_id = ?, name = ? WHERE id = ?',
                    (player.team_id, player.name, player.id)
                )
                return player.id

    def get_player(self, player_id: int) -> Optional[Player]:
        """Get a player by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, team_id, name FROM players WHERE id = ?', (player_id,))
            row = cursor.fetchone()
            if row:
                return Player(id=row[0], team_id=row[1], name=row[2])
            return None

    def save_week(self, week: Week) -> int:
        """Save a week and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if week.id is None:
                cursor.execute(
                    'INSERT INTO weeks (league_id, week_number, start_date, end_date) VALUES (?, ?, ?, ?)',
                    (week.league_id, week.week_number, week.start_date.isoformat(), week.end_date.isoformat())
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE weeks SET league_id = ?, week_number = ?, start_date = ?, end_date = ? WHERE id = ?',
                    (week.league_id, week.week_number, week.start_date.isoformat(), week.end_date.isoformat(), week.id)
                )
                return week.id

    def get_week(self, week_id: int) -> Optional[Week]:
        """Get a week by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, league_id, week_number, start_date, end_date FROM weeks WHERE id = ?', (week_id,))
            row = cursor.fetchone()
            if row:
                return Week(
                    id=row[0],
                    league_id=row[1],
                    week_number=row[2],
                    start_date=date.fromisoformat(row[3]),
                    end_date=date.fromisoformat(row[4])
                )
            return None

    def save_game(self, game: Game) -> int:
        """Save a game and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if game.id is None:
                cursor.execute(
                    'INSERT INTO games (week_id, team_id, date, opponent_team_id) VALUES (?, ?, ?, ?)',
                    (game.week_id, game.team_id, game.date.isoformat(), game.opponent_team_id)
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE games SET week_id = ?, team_id = ?, date = ?, opponent_team_id = ? WHERE id = ?',
                    (game.week_id, game.team_id, game.date.isoformat(), game.opponent_team_id, game.id)
                )
                return game.id

    def get_game(self, game_id: int) -> Optional[Game]:
        """Get a game by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, week_id, team_id, date, opponent_team_id FROM games WHERE id = ?', (game_id,))
            row = cursor.fetchone()
            if row:
                return Game(
                    id=row[0],
                    week_id=row[1],
                    team_id=row[2],
                    date=date.fromisoformat(row[3]),
                    opponent_team_id=row[4]
                )
            return None

    def game_exists(self, league: str, team: str, season: str, game: str) -> bool:
        """Check if a game already exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT g.id FROM games g
                JOIN weeks w ON g.week_id = w.id
                JOIN leagues l ON w.league_id = l.id
                JOIN teams t ON g.team_id = t.id
                WHERE l.name = ? AND t.name = ? AND l.season = ? AND w.week_number = ?
            ''', (league, team, season, int(game)))
            return cursor.fetchone() is not None

    def delete_game_data(self, league: str, team: str, season: str, game: str) -> None:
        """Delete all data for a specific game."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Find the game ID
            cursor.execute('''
                SELECT g.id FROM games g
                JOIN weeks w ON g.week_id = w.id
                JOIN leagues l ON w.league_id = l.id
                JOIN teams t ON g.team_id = t.id
                WHERE l.name = ? AND t.name = ? AND l.season = ? AND w.week_number = ?
            ''', (league, team, season, int(game)))

            game_row = cursor.fetchone()
            if not game_row:
                return  # Game doesn't exist, nothing to delete

            game_id = game_row[0]

            # Delete at-bats for this game
            cursor.execute('DELETE FROM at_bats WHERE game_id = ?', (game_id,))

            # Delete the game
            cursor.execute('DELETE FROM games WHERE id = ?', (game_id,))

            # Note: We don't delete leagues, teams, weeks, or players as they might be used by other games
            # In a more sophisticated system, you might implement cascading deletes or cleanup logic

    def save_at_bat(self, attempt: AtBatAttempt) -> int:
        """Save an at-bat attempt and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if attempt.id is None:
                cursor.execute(
                    'INSERT INTO at_bats (player_id, game_id, outcome, bases, rbis, runs_scored) VALUES (?, ?, ?, ?, ?, ?)',
                    (attempt.player_id, attempt.game_id, attempt.outcome, attempt.bases, attempt.rbis, attempt.runs_scored)
                )
                return cursor.lastrowid
            else:
                cursor.execute(
                    'UPDATE at_bats SET player_id = ?, game_id = ?, outcome = ?, bases = ?, rbis = ?, runs_scored = ? WHERE id = ?',
                    (attempt.player_id, attempt.game_id, attempt.outcome, attempt.bases, attempt.rbis, attempt.runs_scored, attempt.id)
                )
                return attempt.id

    def get_player_stats(self, player_id: int, week_id: Optional[int] = None) -> Optional[PlayerStats]:
        """Get calculated stats for a player, optionally for a specific week."""
        # This is a simplified implementation - in practice you'd aggregate from at_bats table
        # For now, return None
        return None

    def save_game_data(self, objects: Dict[str, Any]) -> None:
        """Save all game data objects in the correct order."""
        # Save in dependency order: league -> team -> week -> game -> players -> at_bats

        # Save league
        league = objects['league']
        league_id = self.save_league(league)
        league.id = league_id

        # Update team with league_id and save
        team = objects['team']
        team.league_id = league_id
        team_id = self.save_team(team)
        team.id = team_id

        # Update week with league_id and save
        week = objects['week']
        week.league_id = league_id
        week_id = self.save_week(week)
        week.id = week_id

        # Update game with week_id and team_id and save
        game = objects['game']
        game.week_id = week_id
        game.team_id = team_id
        game_id = self.save_game(game)
        game.id = game_id

        # Update players with team_id and save
        player_id_map = {}
        for player in objects['players']:
            player.team_id = team_id
            player_id = self.save_player(player)
            player.id = player_id
            player_id_map[player.name] = player_id

        # Update at-bats with player_id and game_id and save
        for attempt_data in objects['attempts']:
            player_id = player_id_map[attempt_data['player_name']]
            attempt = AtBatAttempt(
                id=None,
                player_id=player_id,
                game_id=game_id,
                outcome=attempt_data['outcome'],
                bases=attempt_data['bases'],
                rbis=attempt_data['rbis'],
                runs_scored=attempt_data['runs_scored']
            )
            self.save_at_bat(attempt)

    def save_parsing_warnings(self, warnings: List[Dict[str, Any]]) -> None:
        """Save parsing warnings to the database."""
        if not warnings:
            return

        with self._get_connection() as conn:
            cursor = conn.cursor()
            for warning in warnings:
                cursor.execute('''
                    INSERT INTO parsing_warnings 
                    (player_name, row_num, col_num, filename, original_attempt, assumption)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    warning['player_name'],
                    warning['row_num'],
                    warning['col_num'],
                    warning['filename'],
                    warning['original_attempt'],
                    warning['assumption']
                ))