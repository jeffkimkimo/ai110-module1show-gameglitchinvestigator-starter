from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- Starter tests: check_guess outcome ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- New tests targeting the bugs we fixed ---

def test_check_guess_handles_string_secret():
    # BUG FIX: secret was being cast to str on even attempts, which broke the
    # int comparison. check_guess must work even if secret arrives as a string.
    assert check_guess(60, "50") == "Too High"
    assert check_guess(40, "50") == "Too Low"
    assert check_guess(50, "50") == "Win"


def test_parse_guess_valid_and_invalid():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("42.9") == (True, 42, None)  # floats are truncated
    ok, value, err = parse_guess("hello")
    assert ok is False and value is None and err == "That is not a number."
    ok, value, err = parse_guess("")
    assert ok is False and err == "Enter a guess."


def test_update_score_wrong_guess_does_not_change_score():
    # BUG FIX: wrong guesses used to randomly +5/-5. They should not move score.
    assert update_score(100, "Too High", 2) == 100
    assert update_score(100, "Too Low", 3) == 100


def test_update_score_win_rewards_fewer_attempts():
    # First-attempt win is worth more than a later win, with a floor of 10.
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 50) == 10  # floored at 10


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 500)
    assert get_range_for_difficulty("???") == (1, 100)  # unknown -> default
