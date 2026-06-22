"""Core game logic for the Number Guessing Game.

These functions are pure (no Streamlit, no UI) so they can be unit-tested
with pytest. app.py imports them and handles only the UI / state.
"""


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    # Default to Normal if an unknown difficulty is passed.
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()
    try:
        # Accept "42" and "42.0" but reject non-numeric text.
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: compare as integers so int-vs-str never reaches a broken fallback,
    #      and report the *correct* direction.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    A win awards more points the fewer attempts it took (min 10).
    Wrong guesses never change the score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: a wrong guess should not randomly add or subtract points.
    return current_score
