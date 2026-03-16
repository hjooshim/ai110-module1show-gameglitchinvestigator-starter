import json
from pathlib import Path

# FIX: Refactored core logic from app.py into logic_utils.py using Copilot Agent mode
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: Hint messages were swapped (Too High said Go HIGHER, Too Low said Go LOWER)
    # FIX: Corrected swapped hint messages (Too High -> Go LOWER, Too Low -> Go HIGHER) using Copilot Agent mode
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def load_game_log(file_path, max_entries=10):
    """Load the last `max_entries` games from a JSON log file."""
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            return []
        return data[-max_entries:]
    except Exception:
        return []


def append_game_log(file_path, entry: dict, max_entries=10):
    """Append a new entry to the game log (stored as a JSON array)."""
    path = Path(file_path)
    log = load_game_log(path, max_entries=max_entries)
    log.append(entry)
    # keep only the most recent entries
    log = log[-max_entries:]
    path.write_text(json.dumps(log, indent=2))
    return log


def clear_game_log(file_path):
    """Clear the saved game log file and return an empty list."""
    path = Path(file_path)
    if path.exists():
        path.unlink()
    return []


def get_best_scores(file_path):
    """Return best score per difficulty based on the saved game log."""
    log = load_game_log(file_path, max_entries=1000)
    best = {}
    for entry in log:
        diff = entry.get("difficulty")
        score = entry.get("score")
        if diff is None or score is None:
            continue
        # prefer higher score, tie-break on fewer attempts
        current = best.get(diff)
        if current is None or score > current["score"] or (
            score == current["score"] and entry.get("attempts", 0) < current.get("attempts", 0)
        ):
            best[diff] = {"score": score, "attempts": entry.get("attempts", 0)}
    return best
