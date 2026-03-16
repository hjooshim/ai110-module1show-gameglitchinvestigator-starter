# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, it looked simple and playable, but the rules did not match what the game was actually doing.

1. I noticed was that the secret answer could end up outside the selected difficulty range, because I expected the answer to stay within that mode's limits, but the actual secret number could be generated from a different range.
2. The screen always told me to "Guess a number between 1 and 100," even when I changed to a difficulty with a different range, so I expected the instructions to update with the selected level but they stayed the same.
3. I also noticed that Hard mode was set to 1 to 50 while Normal mode was 1 to 100, so I expected Hard to be more difficult than Normal, but it actually gave a smaller range and made the game easier.
4. I noticed that when my guess was too high, the hint said "Go HIGHER!", but I expected it to tell me to guess lower since it was already too high.
5. When I started a new game, the secret number was always between 1 and 100, even on Easy or Hard mode, so I expected it to respect the difficulty range like the first game did.
6. The attempts counter started at 1 for the first game but reset to 0 for new games, so I expected it to be consistent and always start at 0 to show the correct attempts left.
7. I clicked "New Game" and it did nothing, because the game status (won/lost) was never reset, so the UI immediately stopped the session again.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used GitHub Copilot as my primary AI tool, including its Agent Mode (specifically the Explore subagent) for code exploration and refactoring suggestions.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - The AI suggested refactoring core game logic functions (get_range_for_difficulty, parse_guess, check_guess, update_score) from app.py into logic_utils.py to separate UI code from game logic, and fixing the hint messages in check_guess by swapping "Go HIGHER!" for "Too High" to "Go LOWER!" and vice versa. This was correct as it improved code organization and fixed misleading hints. I verified by running the refactored code: check_guess(60, 50) returned ("Too High", "📉 Go LOWER!"), and the app imported functions successfully from logic_utils.py.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - The AI initially suggested that the new game button already respected the difficulty range for generating the secret number, implying no fix was needed. This was incorrect because the code hardcoded random.randint(1, 100). I verified by examining the code in app.py, where the new_game handler used 1-100 instead of low-high, and tested that after the fix, it used the correct range.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I decided a bug was fixed by running targeted tests on the affected functions and observing the output in the terminal or app behavior. For example, after fixing the hint messages, I manually executed check_guess with different inputs and confirmed the messages matched expectations. If the app ran without errors and the logic behaved correctly, I considered it resolved.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - I ran a manual test by importing check_guess from logic_utils and calling it with arguments like check_guess(60, 50), which returned ("Too High", "📉 Go LOWER!"). This showed that the hint messages were now correct (previously it would have said "Go HIGHER!"), confirming the fix for the misleading hints. I also tested get_range_for_difficulty to ensure ranges were accurate for each difficulty level.
  - I verified the "New Game" action by checking that it resets status, score, attempts, and history; this fixed the bug where clicking the button appeared to do nothing because the game was still flagged as won/lost.
- Did AI help you design or understand any tests? How?
  - The AI helped by suggesting the refactoring structure, which made it easier to isolate and test individual functions in logic_utils.py. It also prompted me to verify the fixes through manual execution, as automated tests weren't fully set up. This collaboration ensured I focused on testing the core logic separately from the UI.
## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Streamlit reruns are like hitting refresh on a webpage every time you interact with it—any button click or input change causes the entire Python script to execute from top to bottom, rebuilding the UI dynamically. Session state is like a persistent backpack for your app's data; it stores variables (like the secret number or attempts) across these reruns using st.session_state, so your game doesn't forget the score or reset the secret on every guess. Without session state, variables would vanish each rerun, making interactive apps impossible.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I want to reuse the habit of running manual tests immediately after code changes, like executing functions in the terminal to verify outputs before full app testing. This quick feedback loop caught issues early and built confidence in fixes.

- What is one thing you would do differently next time you work with AI on a coding task?
  Next time, I'd provide more specific prompts from the start, including exact file references and expected outputs, to reduce the chance of AI making incorrect assumptions (like thinking the new game range was already correct).

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project showed me that AI-generated code is a great starting point but requires thorough verification and testing, as subtle bugs (like swapped messages) can slip through. It made me more proactive in questioning AI suggestions and using them as collaborators rather than infallible tools.
