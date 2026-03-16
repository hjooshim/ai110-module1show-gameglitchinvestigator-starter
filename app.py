import datetime
import random
import streamlit as st
# FIX: Imported refactored functions from logic_utils.py using Copilot Agent mode
from logic_utils import (
    append_game_log,
    clear_game_log,
    get_best_scores,
    get_range_for_difficulty,
    load_game_log,
    parse_guess,
    check_guess,
    update_score,
)

# New Feature: Game session log tracks recent plays and saves them to disk (game_log.json)
# (Added after discussion with an AI agent to make the game more replayable and inspectable.)
GAME_LOG_PATH = "game_log.json"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_log" not in st.session_state:
    st.session_state.game_log = load_game_log(GAME_LOG_PATH, max_entries=10)

st.sidebar.markdown("### Recent games")
for entry in reversed(st.session_state.game_log):
    st.sidebar.markdown(
        f"- **{entry['result']}** ({entry['difficulty']}) — {entry['score']} points, "
        f"{entry['attempts']} attempts — {entry['timestamp']}"
    )

best_scores = get_best_scores(GAME_LOG_PATH)
if best_scores:
    st.sidebar.markdown("### Best scores")
    for difficulty, record in best_scores.items():
        st.sidebar.markdown(
            f"- **{difficulty}**: {record['score']} pts ({record['attempts']} attempts)"
        )

if st.sidebar.button("Clear history"):
    st.session_state.game_log = clear_game_log(GAME_LOG_PATH)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# FIX: Updated instruction text to use dynamic difficulty range instead of hardcoded 1-100
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # Reset all relevant session state so the new game actually starts fresh
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.status = "playing"

    # FIXME: Secret was hardcoded to 1-100 instead of difficulty range
    # FIX: Changed secret generation to use difficulty range instead of hardcoded 1-100 using Copilot Agent mode
    st.session_state.secret = random.randint(low, high)

    st.success("New game started.")
    try:
        st.rerun()
    except AttributeError:
        # Streamlit versions before 1.0 used experimental_rerun
        st.experimental_rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"

            # New feature: append this completed game to the saved log
            st.session_state.game_log = append_game_log(
                GAME_LOG_PATH,
                {
                    "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                    "difficulty": difficulty,
                    "result": "Win",
                    "attempts": st.session_state.attempts,
                    "score": st.session_state.score,
                },
                max_entries=10,
            )

            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"

                # New feature: append this completed game to the saved log
                st.session_state.game_log = append_game_log(
                    GAME_LOG_PATH,
                    {
                        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                        "difficulty": difficulty,
                        "result": "Loss",
                        "attempts": st.session_state.attempts,
                        "score": st.session_state.score,
                    },
                    max_entries=10,
                )

                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
