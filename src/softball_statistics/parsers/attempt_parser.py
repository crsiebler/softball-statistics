import re
from typing import Dict


class AttemptParseError(Exception):
    """Raised when an attempt string cannot be parsed."""
    pass


def parse_attempt(attempt: str, player_name: str = "", row_num: int = 0, 
                 col_num: int = 0, filename: str = "") -> Dict:
    """
    Parse an at-bat attempt string.

    Args:
        attempt: The attempt string (e.g., "2B*", "K", "1B+", "F4")
        player_name: Name of the player (for warnings)
        row_num: Row number in CSV (for warnings)
        col_num: Column number in CSV (for warnings)
        filename: Filename (for warnings)

    Returns:
        Dictionary with keys: 'hit_type', 'bases', 'rbis', 'runs_scored', 'warnings'

    Raises:
        AttemptParseError: If attempt string is invalid
    """
    if not attempt:
        raise AttemptParseError("Attempt string cannot be empty")

    # Convert to lowercase and remove all whitespace
    attempt = ''.join(attempt.split()).lower()

    if not attempt:
        raise AttemptParseError("Attempt string cannot be only whitespace")

    # Define hit type mappings
    hit_types = {
        '1b': ('single', 1),
        '2b': ('double', 2),
        '3b': ('triple', 3),
        'hr': ('home_run', 4),
    }

    # Special cases for outs
    special_outs = ['hpo', 'fo', 'hro']

    # Count modifiers
    rbis = attempt.count('*')
    runs_scored = attempt.count('+')

    # Remove modifiers to get the base attempt
    base_attempt = attempt.replace('*', '').replace('+', '')

    # Parse the base attempt
    if base_attempt in hit_types:
        hit_type, bases = hit_types[base_attempt]
    elif base_attempt == 'k':
        hit_type, bases = 'out', 0  # Strikeout is an out
    elif base_attempt == 'bb':
        hit_type, bases = 'walk', 0
    elif base_attempt in special_outs:
        hit_type, bases = 'out', 0
    elif _is_out_notation(base_attempt):
        hit_type, bases = 'out', 0
    else:
        raise AttemptParseError(f"Unknown attempt notation: '{base_attempt}'")

    # Special HR handling
    warnings = []
    if base_attempt == 'hr':
        if rbis > 4:
            raise AttemptParseError(f"Home runs cannot have more than 4 RBIs: '{attempt}'")
        
        # Auto-correct solo HRs
        if rbis == 0:
            rbis = 1
            runs_scored = max(runs_scored, 1)
            warning_msg = f"ASSUMPTION: Player '{player_name}' HR solo"
            if row_num and col_num and filename:
                warning_msg += f" (row {row_num}, column {col_num} in {filename})"
            warnings.append({
                'player_name': player_name,
                'row_num': row_num,
                'col_num': col_num,
                'filename': filename,
                'original_attempt': attempt,
                'assumption': "HR solo (assumed 1 RBI, 1 run scored)"
            })
        elif rbis == 1 and runs_scored == 0:
            runs_scored = 1
            warning_msg = f"ASSUMPTION: Player '{player_name}' HR solo"
            if row_num and col_num and filename:
                warning_msg += f" (row {row_num}, column {col_num} in {filename})"
            warnings.append({
                'player_name': player_name,
                'row_num': row_num,
                'col_num': col_num,
                'filename': filename,
                'original_attempt': attempt,
                'assumption': "HR solo (assumed 1 RBI, 1 run scored)"
            })

    # Check for invalid consecutive same modifiers (2+ in a row)
    # Skip this check for HR since HR**** is valid (4 RBIs)
    if base_attempt != 'hr' and re.search(r'\*\*{2,}|\+{2,}', attempt):
        raise AttemptParseError(f"Invalid consecutive same modifiers in '{attempt}'")

    # Limit total modifiers to reasonable amounts
    if attempt.count('*') > 4 or attempt.count('+') > 4:
        raise AttemptParseError(f"Too many modifiers in '{attempt}' (max 4 of each type)")

    return {
        'hit_type': hit_type,
        'bases': bases,
        'rbis': rbis,
        'runs_scored': runs_scored,
        'warnings': warnings
    }


def _is_out_notation(attempt: str) -> bool:
    """
    Check if an attempt string represents an out.

    Valid out notations include:
    - Fly balls: F followed by number (F4, F8, etc.)
    - Ground balls: number-number (5-1, 6-4, etc.)
    - Other common out notations: A1, P3, etc.
    - Simple fielding positions: single digit (4, 8, etc.) - assumed to be fly balls
    """
    # Fly ball: F followed by 1-9 (case insensitive)
    if re.match(r'^f[1-9]$', attempt):
        return True

    # Ground ball: number-number (like 5-1, 6-4, 4-3)
    if re.match(r'^\d-\d$', attempt):
        return True

    # Simple fielding position: just a number (4, 8, etc.) - assume fly ball
    if re.match(r'^\d$', attempt):
        return True

    # Other out notations: single character + number, or other common patterns
    # This is more permissive to handle various league notations
    if re.match(r'^[a-z]\d+$', attempt) and len(attempt) <= 3:
        return True

    return False