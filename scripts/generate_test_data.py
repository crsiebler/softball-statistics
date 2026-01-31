#!/usr/bin/env python3
"""
Generate fake softball game data for testing multiple leagues, seasons, and roster changes.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# League and season configuration
LEAGUES = {
    "pacific": {
        "spring-2024": {"start_date": "2024-03-01", "games": 5},
        "fall-2024": {"start_date": "2024-09-01", "games": 5},
    },
    "mountain": {
        "summer-2024": {"start_date": "2024-06-01", "games": 5},
        "winter-2024": {"start_date": "2024-11-01", "games": 5},
    },
}

TEAMS = ["sharks", "bears"]

# Initial players per team (10 players each)
INITIAL_PLAYERS = {
    "sharks": [
        "Alex Rivera",
        "Jordan Chen",
        "Taylor Morgan",
        "Casey Wong",
        "Riley Patel",
        "Morgan Lee",
        "Jamie Torres",
        "Avery Kim",
        "Drew Johnson",
        "Sam Rodriguez",
    ],
    "bears": [
        "Blake Thompson",
        "Logan Garcia",
        "Skyler Davis",
        "Reese Nguyen",
        "Cameron Smith",
        "Peyton Brown",
        "Charlie Wilson",
        "Quinn Martinez",
        "Frank Robinson",
        "Dana Lewis",
    ],
}

# Additional player pool for roster changes
FREE_AGENTS = [
    "Hunter Adams",
    "Parker White",
    "Dakota Black",
    "River Green",
    "Sage Blue",
    "Robin Gray",
    "Phoenix Red",
    "Storm Yellow",
    "Willow Purple",
    "Ash Orange",
    "Brook Pink",
    "Gale Brown",
    "Finch Gold",
    "Sparrow Silver",
    "Jay Bronze",
    "Owl Copper",
]

# Outcomes for randomization
OUTCOMES = [
    "1B",
    "2B",
    "3B",
    "HR",
    "K",
    "BB",
    "HPO",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "1-3",
    "4-3",
    "5-3",
    "6-3",
    "6-4",
    "6-5",
]


# Weights for realistic softball outcomes (approximate % of plate appearances)
# - 1B: 36% (most common hit)
# - 2B: 10% (moderate doubles)
# - 3B: 0.5% (rare triples)
# - HR: 4% (power hit, less common than doubles)
# - K: 5% (low strikeouts in softball)
# - BB: 6% (moderate walks)
# - HPO: 1% (rare hit by pitch)
# - F1-F10: 1.6% each (~16% fly outs total to various fielders)
# - 1-3,4-3,5-3,6-3,6-4,6-5: 3.1% each (~19% groundouts total)
WEIGHTS = [
    36,
    10,
    0.5,
    4,
    5,
    6,
    1,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    1.6,
    3.1,
    3.1,
    3.1,
    3.1,
    3.1,
    3.1,
]


def get_advance_bases(outcome):
    """Return number of bases to advance on this outcome."""
    if outcome in ["1B", "2B", "3B", "HR"]:
        return {"1B": 1, "2B": 2, "3B": 3, "HR": 4}[outcome]
    elif outcome == "BB":
        return 1
    elif outcome in ["K", "HPO"]:
        return 0  # no advance on these outs
    else:
        # other outs: random 0-3, biased toward 0
        weights = [
            0.85,
            0.13,
            0.015,
            0.005,
        ]  # heavily bias toward 0, almost none to 2/3
        return random.choices([0, 1, 2, 3], weights=weights)[0]


def is_out(outcome):
    """Check if outcome is an out."""
    if outcome in ["1B", "2B", "3B", "HR", "BB"]:
        return False
    return True


def is_hit(outcome):
    """Check if outcome is a hit."""
    return outcome in ["1B", "2B", "3B", "HR"]


class InningSimulator:
    """Simulates a single inning with runner tracking."""

    def __init__(self, lineup):
        self.lineup = lineup  # list of player indices
        self.bases = {1: None, 2: None, 3: None}  # base: player_idx or None
        self.outs = 0
        self.attempts = {
            i: [] for i in range(len(lineup))
        }  # player_idx: list of outcomes
        self.lineup_idx = 0

    def advance_runners(self, advance_bases, batter_idx, outcome):
        """Advance runners based on outcome, return runs scored and rbis."""
        runs_scored = 0
        rbis = 0
        scoring_runners = []  # runners who score

        # New runners dict to avoid modifying while iterating
        new_bases = {1: None, 2: None, 3: None}

        # Place batter on base if hit/walk
        if not is_out(outcome):
            batter_base = advance_bases
            if batter_base == 4:  # HR, scores immediately
                runs_scored += 1
                rbis += 1  # HR always 1 RBI unless no runners, but we count it
                scoring_runners.append(batter_idx)
            else:
                # Place batter on appropriate base
                new_bases[batter_base] = batter_idx

        # Advance existing runners
        for base in [3, 2, 1]:  # reverse order to avoid overwriting
            if self.bases[base] is not None:
                runner = self.bases[base]
                new_base = base + advance_bases
                if new_base >= 4:  # scores
                    runs_scored += 1
                    rbis += 1  # each scoring runner is an RBI
                    scoring_runners.append(runner)
                else:
                    new_bases[new_base] = runner

        self.bases = new_bases
        return runs_scored, rbis, scoring_runners

    def simulate_plate_appearance(self):
        """Simulate one plate appearance, return outcome with modifiers."""
        batter_idx = self.lineup[self.lineup_idx % len(self.lineup)]
        self.lineup_idx += 1

        outcome = random.choices(OUTCOMES, weights=WEIGHTS)[0]
        advance_bases = get_advance_bases(outcome)

        runs_scored, rbis, scoring_runners = self.advance_runners(
            advance_bases, batter_idx, outcome
        )

        # Apply modifiers
        modified_outcome = outcome
        if rbis > 0:
            # Cap RBIs: HR max 4, others max 3 if bases loaded
            max_rbi = 4 if outcome == "HR" else 3
            rbi_to_add = min(rbis, max_rbi)
            modified_outcome += "*" * rbi_to_add

        # HR always scores a run for the batter
        if outcome == "HR":
            modified_outcome += "+"

        # For runs scored by runners, add '+' to their outcomes
        for runner_idx in scoring_runners:
            if runner_idx != batter_idx:  # batter's run is not a '+' modifier
                # Find the runner's last attempt and add '+'
                if self.attempts[runner_idx]:
                    last_attempt = self.attempts[runner_idx][-1]
                    if not last_attempt.endswith("+"):
                        self.attempts[runner_idx][-1] = last_attempt + "+"

        self.attempts[batter_idx].append(modified_outcome)

        if is_out(outcome):
            self.outs += 1

        return runs_scored, rbis

    def simulate_inning(self):
        """Simulate until 3 outs."""
        self.outs = 0  # Reset outs for new inning
        self.bases = {1: None, 2: None, 3: None}  # Reset bases for new inning
        while self.outs < 3:
            self.simulate_plate_appearance()


def simulate_game_innings(num_players):
    """Simulate a game with multiple innings, return attempts per player."""
    lineup = list(range(num_players))  # player indices 0 to num_players-1
    simulator = InningSimulator(lineup)  # One simulator per game to persist lineup_idx

    num_innings = random.randint(5, 7)

    for inning in range(num_innings):
        simulator.simulate_inning()

    return simulator.attempts


def get_date_range(start_date_str, num_games):
    """Generate weekly dates starting from start_date."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    dates = []
    for i in range(num_games):
        game_date = start_date + timedelta(weeks=i)
        dates.append(game_date.strftime("%Y-%m-%d"))
    return dates


def simulate_roster_changes(current_roster, season_order):
    """Apply roster changes based on season progression."""
    roster = current_roster.copy()

    if season_order == 0:  # First season, no changes
        return roster

    # Apply changes: some leave, some join, some return
    num_changes = random.randint(1, 3)

    # Players leaving
    leavers = random.sample(roster, min(num_changes, len(roster)))
    for player in leavers:
        roster.remove(player)

    # New free agents joining
    joiners = random.sample(FREE_AGENTS, min(num_changes, len(FREE_AGENTS)))
    roster.extend(joiners)

    # Some old players returning (if available)
    available_returnees = [
        p
        for p in INITIAL_PLAYERS["sharks"] + INITIAL_PLAYERS["bears"]
        if p not in roster
    ]
    if available_returnees:
        returnees = random.sample(available_returnees, min(1, len(available_returnees)))
        roster.extend(returnees)

    # Ensure we have at least 8 players
    while len(roster) < 8:
        new_player = random.choice(FREE_AGENTS)
        if new_player not in roster:
            roster.append(new_player)

    return roster


def generate_game_attempts(num_players, avg_attempts=5):
    """Generate attempts for a game using inning simulation."""
    all_attempts = simulate_game_innings(num_players)

    # Convert to list of lists, pad/truncate to 7 attempts per player
    attempts = []
    for player_idx in range(num_players):
        player_attempts = all_attempts[player_idx]
        # Pad or truncate to exactly 7 attempts
        while len(player_attempts) < 7:
            player_attempts.append("")
        attempts.append(player_attempts[:7])

    return attempts


def main():
    output_dir = Path(__file__).parent / "../data/test/input"
    output_dir.mkdir(parents=True, exist_ok=True)

    season_order = 0

    for league, seasons in LEAGUES.items():
        for season, config in seasons.items():
            dates = get_date_range(config["start_date"], config["games"])

            for team in TEAMS:
                # Get current roster for this season
                if season_order == 0:
                    roster = INITIAL_PLAYERS[team].copy()
                else:
                    roster = simulate_roster_changes(
                        INITIAL_PLAYERS[team], season_order
                    )

                for game_num in range(1, config["games"] + 1):
                    date = dates[game_num - 1]

                    # Generate game data
                    attempts = generate_game_attempts(len(roster))

                    # Create CSV
                    # Generate filename (season without year, parser adds it from date)
                    season_name_only = season.split("-")[
                        0
                    ]  # Remove year from season for filename
                    filename = (
                        f"{league}-{team}-{season_name_only}-{game_num:02d}_{date}.csv"
                    )
                    filepath = output_dir / filename

                    with open(filepath, "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)

                        # Header
                        writer.writerow(["Player Name"] + [f"Attempt"] * 7)

                        # Player data
                        for player, player_attempts in zip(roster, attempts):
                            writer.writerow([player] + player_attempts)

                    print(f"Generated: {filename}")
        season_order += 1


if __name__ == "__main__":
    main()
