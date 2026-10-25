"""STATEFUL QUIZ APP"""

import streamlit as st


st.set_page_config(page_title="Stateful Quiz App", page_icon="📝", layout="wide")

# ── Step 1: Quiz data ──────────────────────────────────────────────────────
# TODO: Create a list called QUESTIONS with 5 dicts.
# Each dict should have:
#   "question"    : str  — the question text
#   "options"     : list — 4 answer choices
#   "answer"      : str  — must match exactly one of the options
#   "explanation" : str  — shown after the user answers
QUESTIONS = [
    {
        "question": "What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Hyper Transfer Markup Language",
            "Home Tool Markup Language"
        ],
        "answer": 0,
        "explanation": "HTML stands for Hyper Text Markup Language and structures web pages."
    },
    {
        "question": "Which CSS property changes the text color?",
        "options": [
            "font-style",
            "background-color",
            "color",
            "text-decoration"
        ],
        "answer": 2,
        "explanation": "The color property changes the text color of an HTML element."
    },
    {
        "question": "Which JavaScript method selects an element by its ID?",
        "options": [
            "document.querySelectorAll()",
            "document.getElementById()",
            "document.createElement()",
            "document.getElementsByClassName()"
        ],
        "answer": 1,
        "explanation": "document.getElementById() selects an element using its unique ID."
    },
    {
        "question": "Which Python data type stores key-value pairs?",
        "options": [
            "List",
            "Tuple",
            "Set",
            "Dictionary"
        ],
        "answer": 3,
        "explanation": "A dictionary stores data as key-value pairs."
    },
    {
        "question": "Which HTTP method is typically used to retrieve data from an API?",
        "options": [
            "POST",
            "DELETE",
            "GET",
            "PATCH"
        ],
        "answer": 2,
        "explanation": "GET requests retrieve information from an API."
    }
]


# ── Step 2: Session state initialisation ──────────────────────────────────
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected" not in st.session_state:
    st.session_state.selected = None

if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ── Step 3: Page config ───────────────────────────────────────────────────
# TODO: st.set_page_config and st.title

st.title("🧠 Coding Temple Knowledge Quiz")

# ══════════════════════════════════════════════════════════════════════════
# RESULTS SCREEN
# Render when st.session_state.show_results is True
# ══════════════════════════════════════════════════════════════════════════
# TODO: $if st.session_state.show_results:
#   - Calculate percentage score
#   - Show st.success / st.warning based on score
#   - Show st.progress(pct / 100)
#   - Show a Restart button that resets all session state keys
#   - Call st.stop() so the quiz below doesn't render
#   - Call st.rerun() after resetting state to refresh the page
if st.session_state.show_results:
    st.subheader("🏆 Quiz Complete!")

    total_questions = len(QUESTIONS)
    score = st.session_state.score
    percentage = (score / total_questions) * 100

    st.metric("Final Score", f"{score}/{total_questions}")
    st.progress(percentage / 100)

    if percentage >= 70:
        st.success(f"Great job! You scored {percentage:.0f}%!")
    else:
        st.warning(f"You scored {percentage:.0f}%. Keep practicing!")

    if st.button("🔄 Restart Quiz"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected = None
        st.session_state.show_results = False
        st.rerun()

    st.stop()
# ══════════════════════════════════════════════════════════════════════════
# QUIZ SCREEN
# ══════════════════════════════════════════════════════════════════════════
# TODO: Get the current question from QUESTIONS[st.session_state.current_q]

# TODO: Show progress indicator: "Question X of 5"
# TODO: Show st.progress(q_index / total_qs)

# TODO: Show st.subheader with the question text

# TODO: Show st.radio with the answer options
#   - Use disabled=True after the user has submitted (st.session_state.answered)
#   - Give it a unique key per question: key=f"q_{q_index}"
#   - Store the selection in st.session_state.selected

# TODO: If not yet answered: show a Submit button
#   - On click: set st.session_state.answered = True
#   - If correct: increment st.session_state.score
#   - Call st.rerun() to trigger a re-render showing feedback

# TODO: If answered: show feedback
#   - st.success if correct, st.error if wrong (show the correct answer)
#   - st.info with the explanation
#   - Show a Next / Finish button
#     - If last question: set show_results = True, call st.rerun()
#     - Otherwise: increment current_q, reset answered/selected, call st.rerun()


# --- Add answer selection ---
q_index = st.session_state.current_q
total_qs = len(QUESTIONS)

question = QUESTIONS[q_index]

st.write(f"Question {q_index + 1} of {total_qs}")
st.progress(q_index / total_qs)

st.subheader(question["question"])

selected_answer = st.radio(
    "Choose your answer:",
    question["options"],
    index=None,
    key=f"q_{q_index}",
    disabled=st.session_state.answered
)

if selected_answer is not None and not st.session_state.answered:
    st.session_state.selected = question["options"].index(selected_answer)


# --- Submit Answer ---
if not st.session_state.answered:
    if st.button("Submit Answer"):
        if st.session_state.selected is None:
            st.warning("Please select an answer first.")
        else:
            st.session_state.answered = True

            if st.session_state.selected == question["answer"]:
                st.session_state.score += 1

            st.rerun()



# --- Answer Feedback ---
if st.session_state.answered:

    correct_answer = question["options"][question["answer"]]

    if st.session_state.selected == question["answer"]:
        st.success("Correct! Great job!")
    else:
        st.error(f"Incorrect! The correct answer is: {correct_answer}")

    st.info(
        f"Current Score: {st.session_state.score}/{total_qs}"
    )
    st.info(question["explanation"])
    
    # --- Next Question Button ---
    if st.button("Next Question" if q_index < total_qs - 1 else "Finish Quiz"):

        if q_index == total_qs - 1:
            st.session_state.show_results = True

        else:
            st.session_state.current_q += 1
            st.session_state.answered = False
            st.session_state.selected = None

        st.rerun()