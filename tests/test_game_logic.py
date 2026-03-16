from logic_utils import append_game_log, check_guess, clear_game_log, get_best_scores, load_game_log

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")

def test_check_guess_messages():
    # Test that hint messages are correct after bug fix
    assert check_guess(60, 50) == ("Too High", "📉 Go LOWER!")
    assert check_guess(40, 50) == ("Too Low", "📈 Go HIGHER!")

def test_get_range_for_difficulty():
    from logic_utils import get_range_for_difficulty
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_game_log_persistence(tmp_path):
    # Verify that game logs can be written and read back
    log_file = tmp_path / "game_log.json"
    append_game_log(log_file, {"timestamp": "2026-01-01T00:00:00", "difficulty": "Easy", "result": "Win", "attempts": 3, "score": 50})
    append_game_log(log_file, {"timestamp": "2026-01-01T00:01:00", "difficulty": "Hard", "result": "Loss", "attempts": 5, "score": 10})

    log = load_game_log(log_file)
    assert len(log) == 2
    assert log[0]["result"] == "Win"
    assert log[1]["difficulty"] == "Hard"


def test_clear_game_log(tmp_path):
    # Verify that the log can be cleared
    log_file = tmp_path / "game_log.json"
    append_game_log(log_file, {"timestamp": "2026-01-01T00:00:00", "difficulty": "Easy", "result": "Win", "attempts": 3, "score": 50})
    cleared = clear_game_log(log_file)
    assert cleared == []
    assert not log_file.exists()


def test_get_best_scores(tmp_path):
    # Verify best score selection logic
    log_file = tmp_path / "game_log.json"
    append_game_log(log_file, {"timestamp": "2026-01-01T00:00:00", "difficulty": "Easy", "result": "Win", "attempts": 5, "score": 20})
    append_game_log(log_file, {"timestamp": "2026-01-01T00:02:00", "difficulty": "Easy", "result": "Win", "attempts": 3, "score": 20})
    append_game_log(log_file, {"timestamp": "2026-01-01T00:03:00", "difficulty": "Hard", "result": "Loss", "attempts": 2, "score": 10})

    best = get_best_scores(log_file)
    assert best["Easy"]["score"] == 20
    assert best["Easy"]["attempts"] == 3
    assert best["Hard"]["score"] == 10
