import os

import requests
import streamlit as st


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="AI Knowledge Retention Predictor",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# PROFESSIONAL UI / UX STYLING
# =========================================================

st.markdown("""
<style>

    /* =========================
       Main Application
       ========================= */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef5ff 50%,
            #f8faff 100%
        );
    }

    /* Main content width */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* =========================
       Typography
       ========================= */

    h1 {
        color: #172554 !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #1e40af !important;
        font-weight: 650 !important;
    }

    p, label {
        color: #334155;
    }


    /* =========================
       Navigation
       ========================= */

    div[data-testid="stRadio"] > div {
        gap: 0.7rem;
    }

    div[data-testid="stRadio"] label {
        background: white;
        padding: 0.45rem 0.9rem;
        border-radius: 8px;
        border: 1px solid #dbe4f0;
        transition: all 0.2s ease;
    }

    div[data-testid="stRadio"] label:hover {
        border-color: #60a5fa;
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(30, 64, 175, 0.08);
    }


    /* =========================
       Input Fields
       ========================= */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 9px !important;
        border: 1px solid #d7e0ec !important;
        background-color: #ffffff !important;
        padding: 0.65rem !important;
        transition: all 0.2s ease;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.12) !important;
    }


    /* =========================
       Selectbox
       ========================= */

    div[data-baseweb="select"] > div {
        border-radius: 9px !important;
        border-color: #d7e0ec !important;
        background-color: white !important;
    }


    /* =========================
       Buttons
       ========================= */

    .stButton > button {
        border-radius: 9px !important;
        border: none !important;
        padding: 0.65rem 1.25rem !important;
        font-weight: 650 !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(30, 64, 175, 0.18);
    }

    .stButton > button:active {
        transform: translateY(0);
    }


    /* =========================
       Forms / Cards
       ========================= */

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid #dbe4f0;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 14px !important;
        border: 1px solid #dbe4f0 !important;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
        transition: all 0.25s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 9px 25px rgba(15, 23, 42, 0.09);
    }


    /* =========================
       Metric Cards
       ========================= */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #dbe4f0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
        transition: all 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
    }


    /* =========================
       Alerts
       ========================= */

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }


    /* =========================
       Progress Bars
       ========================= */

    div[data-testid="stProgress"] > div {
        border-radius: 10px;
    }

    div[data-testid="stProgress"] > div > div {
        border-radius: 10px;
    }


    /* =========================
       Quiz Radio Options
       ========================= */

    div[data-testid="stRadio"] label {
        transition: all 0.2s ease;
    }


    /* =========================
       Dividers
       ========================= */

    hr {
        border: none;
        border-top: 1px solid #dbe4f0;
        margin: 1.5rem 0;
    }


    /* =========================
       Subtle Animation
       ========================= */

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .block-container {
        animation: fadeIn 0.4s ease-in-out;
    }

</style>
""", unsafe_allow_html=True)


# =========================
# Session State
# =========================

if "learner_name" not in st.session_state:
    st.session_state.learner_name = ""

if "concepts" not in st.session_state:
    st.session_state.concepts = []

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "analyzed_topic" not in st.session_state:
    st.session_state.analyzed_topic = None

if "quiz_progress" not in st.session_state:
    st.session_state.quiz_progress = 0

if "current_view" not in st.session_state:
    st.session_state.current_view = "Concept Input"


# =========================
# Application Title
# =========================

st.title("🧠 AI Knowledge Retention Predictor")


# =========================
# Navigation
# =========================

view = st.radio(
    "Navigate",
    ["Concept Input", "Analysis Dashboard", "Quiz"],
    horizontal=True
)

st.session_state.current_view = view
API_BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").rstrip("/")


# =========================================================
# CONCEPT INPUT
# =========================================================

if view == "Concept Input":

    st.header("Concept Input")

    learner_name = st.text_input(
        "Learner Name",
        value=st.session_state.learner_name
    )

    st.session_state.learner_name = learner_name

    st.subheader("Add Study Concept")

    with st.form("concept_form"):

        topic = st.text_input("Topic Name")

        last_revision_date = st.date_input(
            "Last Revision Date"
        )

        quiz_score = st.number_input(
            "Quiz Score",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        difficulty = st.selectbox(
            "Difficulty Level",
            ["Easy", "Medium", "Hard"]
        )

        add_concept = st.form_submit_button(
            "Add Concept"
        )

        if add_concept:

            if not topic.strip():

                st.error(
                    "Please enter a topic name."
                )

            elif not learner_name.strip():

                st.error(
                    "Please enter learner name."
                )

            else:

                concept = {
                    "topic": topic,
                    "last_revision_date": str(
                        last_revision_date
                    ),
                    "quiz_score": quiz_score,
                    "difficulty": difficulty
                }

                st.session_state.concepts.append(
                    concept
                )

                st.success(
                    f"{topic} added successfully!"
                )


    # =========================
    # Study Concepts
    # =========================

    st.subheader("Your Study Concepts")

    if st.session_state.concepts:

        for index, concept in enumerate(
            st.session_state.concepts,
            start=1
        ):

            score = concept["quiz_score"]

            if score >= 80:
                mastery = "🟢 Strong"

            elif score >= 50:
                mastery = "🟡 Moderate"

            else:
                mastery = "🔴 Needs Improvement"

            st.markdown(
                f"""
                ### {index}. {concept["topic"]}

                - 📅 Last Revision:
                  {concept["last_revision_date"]}

                - 📝 Quiz Score:
                  {concept["quiz_score"]:.1f}%

                - 🎯 Difficulty:
                  **{concept["difficulty"]}**

                - 🧠 Mastery:
                  **{mastery}**
                """
            )

            if st.button("🗑️ Remove", key=f"remove_concept_{index}"):
                removed_topic = st.session_state.concepts.pop(index - 1)["topic"]
                st.session_state.analysis_results = None
                st.session_state.quiz_questions = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.success(f"{removed_topic} removed successfully.")
                st.rerun()

            st.divider()


        # =========================
        # Retention Analysis
        # =========================

        st.subheader("Retention Analysis")

        concept_names = [c["topic"] for c in st.session_state.concepts]
        selected_topic = st.selectbox(
            "Concept to analyze",
            concept_names,
            key="analysis_topic_selector"
        )
        concept = next(
            c for c in st.session_state.concepts
            if c["topic"] == selected_topic
        )

        if st.button("Analyze Retention", type="primary"):
            payload = {
                "learner_name": st.session_state.learner_name,
                "topic": concept["topic"],
                "last_revision_date": concept["last_revision_date"],
                "quiz_score": concept["quiz_score"],
                "difficulty": concept["difficulty"]
            }

            try:
                with st.spinner("Analyzing knowledge retention..."):
                    response = requests.post(
                        f"{API_BASE_URL}/analyze",
                        json=payload,
                        timeout=30
                    )

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.analysis_results = result
                    st.session_state.analyzed_topic = concept["topic"]
                    st.success("Retention analysis completed successfully!")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Analysis failed: {detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    f"Could not connect to the backend API at {API_BASE_URL}. "
                    "Make sure FastAPI is running."
                )
            except requests.exceptions.Timeout:
                st.error("The analysis request timed out. Please try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    else:

        st.info(
            "No study concepts added yet."
        )


# =========================================================
# ANALYSIS DASHBOARD
# =========================================================

elif view == "Analysis Dashboard":

    st.header(
        "📊 Retention Analysis Dashboard"
    )

    if st.session_state.analysis_results:

        result = st.session_state.analysis_results

        # =========================
        # Last Analyzed Concept
        # =========================

        analyzed_topic = st.session_state.get("analyzed_topic")
        if analyzed_topic:
            concept = next(
                (c for c in st.session_state.concepts if c["topic"] == analyzed_topic),
                {}
            )
        elif st.session_state.concepts:
            concept = st.session_state.concepts[-1]
        else:
            concept = {}

        topic = concept.get(
            "topic",
            "Unknown"
        )

        quiz_score = float(
            concept.get(
                "quiz_score",
                0
            )
        )

        difficulty = concept.get(
            "difficulty",
            "Unknown"
        )


        # =========================
        # Backend Results
        # =========================

        risk = result.get(
            "retention_risk",
            "Not available"
        )

        forgetting_window = result.get(
            "forgetting_window",
            "Not available"
        )

        revision_timing = result.get(
            "revision_timing",
            "Not available"
        )

        study_advice = result.get(
            "study_advice",
            "No advice available"
        )


        # =========================
        # Overall Learning Status
        # =========================

        st.subheader(
            "📈 Overall Learning Status"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📚 Concept",
            topic
        )

        col2.metric(
            "📝 Quiz Score",
            f"{quiz_score:.1f}%"
        )

        col3.metric(
            "🎯 Difficulty",
            difficulty
        )

        col4.metric(
            "⚠️ Retention Risk",
            str(risk)
        )


        st.divider()


        # =========================
        # Quiz Performance
        # =========================

        st.subheader(
            "📊 Learning Performance"
        )

        score_col1, score_col2 = st.columns(
            [2, 1]
        )

        with score_col1:

            st.write(
                "Quiz Performance"
            )

            st.progress(
                int(
                    max(
                        0,
                        min(
                            100,
                            quiz_score
                        )
                    )
                )
            )

            st.caption(
                f"Quiz Score: {quiz_score:.1f}%"
            )

        with score_col2:

            if quiz_score >= 80:

                st.success(
                    "🟢 Strong mastery"
                )

            elif quiz_score >= 50:

                st.warning(
                    "🟡 Moderate mastery"
                )

            else:

                st.error(
                    "🔴 Needs improvement"
                )


        st.divider()


        # =========================
        # Retention Risk
        # =========================

        st.subheader(
            "🎯 Retention Risk"
        )

        risk_lower = str(
            risk
        ).lower()


        if "high" in risk_lower:

            risk_value = 90

            st.error(
                f"🔴 High Retention Risk\n\n{risk}"
            )


        elif "medium" in risk_lower:

            risk_value = 60

            st.warning(
                f"🟡 Medium Retention Risk\n\n{risk}"
            )


        elif "low" in risk_lower:

            risk_value = 25

            st.success(
                f"🟢 Low Retention Risk\n\n{risk}"
            )


        else:

            risk_value = 0

            st.info(
                f"ℹ️ Retention Risk: {risk}"
            )


        st.write(
            "Risk Level"
        )

        st.progress(
            risk_value
        )

        st.caption(
            f"Estimated retention risk level: "
            f"{risk_value}%"
        )


        st.divider()


        # =========================
        # Concept-wise Analysis
        # =========================

        st.subheader(
            "🧠 Concept-wise Retention Analysis"
        )

        with st.container(
            border=True
        ):

            st.markdown(
                f"### 📘 {topic}"
            )

            detail_col1, detail_col2 = st.columns(
                2
            )


            with detail_col1:

                st.markdown(
                    "#### 📅 Forgetting Window"
                )

                st.info(
                    str(forgetting_window)
                )


            with detail_col2:

                st.markdown(
                    "#### 🔄 Recommended Revision Timing"
                )

                st.info(
                    str(revision_timing)
                )


            st.markdown("---")


            st.markdown(
                "#### 💡 Personalized Study Advice"
            )

            st.success(
                str(study_advice)
            )


        st.divider()


        # =========================
        # Retention Summary Chart
        # =========================

        st.subheader(
            "📊 Retention Summary"
        )

        chart_data = {
            "Metric": [
                "Quiz Score",
                "Retention Risk"
            ],

            "Percentage": [
                quiz_score,
                risk_value
            ]
        }

        st.bar_chart(
            chart_data,
            x="Metric",
            y="Percentage"
        )


    else:

        st.info(
            "No retention analysis available yet. "
            "Add a concept and run analysis first."
        )

# =========================================================
# QUIZ
# =========================================================

elif view == "Quiz":

    st.header("📝 Adaptive Quiz")

    # =====================================================
    # QUIZ SESSION STATE
    # =====================================================

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    questions = st.session_state.quiz_questions


    # =====================================================
    # NO QUIZ GENERATED
    # =====================================================

    if not questions:

        if not st.session_state.concepts:

            st.warning(
                "⚠️ Please add a study concept first."
            )

        else:

            concept = st.session_state.concepts[-1]

            topic = concept.get(
                "topic",
                "Unknown"
            )

            difficulty = concept.get(
                "difficulty",
                "Medium"
            )

            st.info(
                "Generate an AI-powered quiz to start "
                "knowledge reinforcement."
            )

            st.write(
                f"**📚 Topic:** {topic}"
            )

            st.write(
                f"**🎯 Difficulty:** {difficulty}"
            )

            st.write(
                "**📝 Questions:** 10"
            )

            if st.button(
                "🚀 Generate Quiz",
                type="primary"
            ):

                analysis = st.session_state.get("analysis_results") or {}
                quiz_payload = {
                    "topic": topic,
                    "difficulty": difficulty,
                    "retention_risk": analysis.get("retention_risk", "Medium"),
                    "forgetting_window": analysis.get("forgetting_window", "3-5 days"),
                    "revision_timing": analysis.get("revision_timing", "Revise within 3 days"),
                    "study_advice": analysis.get(
                        "study_advice",
                        "Review the concept regularly and practice with short quizzes."
                    ),
                    "num_questions": 10
                }

                try:

                    with st.spinner(
                        "🤖 Generating your AI quiz..."
                    ):

                        response = requests.post(
                            f"{API_BASE_URL}/quiz",
                            json=quiz_payload,
                            timeout=60
                        )

                    if response.status_code == 200:

                        data = response.json()

                        quiz = data.get(
                            "quiz",
                            {}
                        )

                        generated_questions = quiz.get(
                            "questions",
                            []
                        )

                        if generated_questions:

                            st.session_state.quiz_questions = (
                                generated_questions
                            )

                            st.session_state.quiz_answers = {}

                            st.session_state.quiz_submitted = False

                            st.session_state.quiz_score = 0

                            st.success(
                                "✅ Quiz generated successfully!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Quiz was generated but "
                                "no questions were returned."
                            )

                    else:

                        try:

                            error_data = response.json()

                            error_message = error_data.get(
                                "detail",
                                "Unknown error"
                            )

                        except Exception:

                            error_message = response.text

                        st.error(
                            f"❌ Quiz generation failed: "
                            f"{error_message}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to backend API. "
                        "Make sure FastAPI is running on port 8000."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ Quiz generation timed out. "
                        "Please try again."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unexpected error: {str(e)}"
                    )


    # =====================================================
    # QUIZ INTERFACE
    # =====================================================

    else:

        total_questions = len(questions)

        answered_questions = len(
            st.session_state.quiz_answers
        )

        progress = (
            answered_questions / total_questions
        )

        st.subheader("📊 Quiz Progress")

        st.progress(progress)

        st.caption(
            f"Answered: {answered_questions}/"
            f"{total_questions}"
        )

        st.divider()


        # =================================================
        # QUESTIONS
        # =================================================

        for index, question_data in enumerate(
            questions
        ):

            question_number = index + 1

            question_text = question_data.get(
                "question",
                f"Question {question_number}"
            )

            options = question_data.get(
                "options",
                {}
            )

            st.subheader(
                f"Question {question_number}"
            )

            st.write(
                f"**{question_text}**"
            )


            # ---------------------------------------------
            # OPTIONS
            # ---------------------------------------------

            option_values = []

            if isinstance(options, dict):

                for key, value in options.items():

                    option_values.append(
                        (key, str(value))
                    )

            elif isinstance(options, list):

                for option_index, option in enumerate(
                    options
                ):

                    key = chr(
                        65 + option_index
                    )

                    if isinstance(option, dict):

                        value = option.get(
                            "label",
                            option.get(
                                "text",
                                str(option)
                            )
                        )

                    else:

                        value = str(option)

                    option_values.append(
                        (key, str(value))
                    )


            # ---------------------------------------------
            # RADIO OPTIONS
            # ---------------------------------------------

            if option_values:

                display_options = [
                    f"{key}. {value}"
                    for key, value in option_values
                ]

                previous_answer = (
                    st.session_state.quiz_answers.get(
                        index
                    )
                )

                default_index = None

                if previous_answer:

                    for option_index, (
                        key,
                        value
                    ) in enumerate(
                        option_values
                    ):

                        if key == previous_answer:

                            default_index = option_index

                            break


                selected_option = st.radio(
                    "Select your answer:",
                    display_options,
                    index=default_index,
                    key=f"quiz_question_{index}"
                )


                if selected_option:

                    selected_key = selected_option[
                        0
                    ]

                    st.session_state.quiz_answers[
                        index
                    ] = selected_key


            st.divider()


        # =================================================
        # SUBMIT QUIZ
        # =================================================

        if not st.session_state.quiz_submitted:

            if st.button(
                "✅ Submit Quiz",
                type="primary"
            ):

                if answered_questions < total_questions:

                    st.warning(
                        f"⚠️ Please answer all "
                        f"{total_questions} questions before submitting."
                    )

                else:

                    score = 0

                    for index, question_data in enumerate(
                        questions
                    ):

                        selected_answer = (
                            st.session_state.quiz_answers.get(
                                index
                            )
                        )

                        correct_answer = str(
                            question_data.get(
                                "correct_answer",
                                ""
                            )
                        ).strip().upper()

                        if selected_answer == correct_answer:

                            score += 1


                    final_score = (
                        score / total_questions
                    ) * 100

                    st.session_state.quiz_score = (
                        final_score
                    )

                    st.session_state.quiz_submitted = (
                        True
                    )

                    st.rerun()


        # =================================================
        # QUIZ RESULTS
        # =================================================

        if st.session_state.quiz_submitted:

            score = st.session_state.quiz_score

            correct_count = round(
                (score / 100) * total_questions
            )

            st.divider()

            st.subheader(
                "🏆 Quiz Result"
            )

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Final Score",
                    f"{score:.1f}%"
                )

            with result_col2:

                st.metric(
                    "Correct Answers",
                    f"{correct_count}/{total_questions}"
                )


            st.progress(
                int(score)
            )


            # ---------------------------------------------
            # PERFORMANCE MESSAGE
            # ---------------------------------------------

            if score >= 80:

                st.success(
                    "🟢 Excellent performance! "
                    "Your knowledge retention is strong."
                )

            elif score >= 50:

                st.warning(
                    "🟡 Good attempt! "
                    "Some concepts may need revision."
                )

            else:

                st.error(
                    "🔴 More revision is recommended "
                    "to strengthen your retention."
                )


            # =================================================
            # QUESTION-WISE FEEDBACK
            # =================================================

            st.subheader(
                "📋 Question-wise Feedback"
            )

            for index, question_data in enumerate(
                questions
            ):

                question_number = index + 1

                question_text = question_data.get(
                    "question",
                    f"Question {question_number}"
                )

                options = question_data.get(
                    "options",
                    {}
                )

                selected_answer = (
                    st.session_state.quiz_answers.get(
                        index
                    )
                )

                correct_answer = str(
                    question_data.get(
                        "correct_answer",
                        ""
                    )
                ).strip().upper()


                # Get correct option text

                if isinstance(options, dict):

                    correct_text = options.get(
                        correct_answer,
                        "Not available"
                    )

                else:

                    correct_text = "Not available"


                if selected_answer == correct_answer:

                    st.success(
                        f"✅ Question {question_number}: Correct"
                    )

                else:

                    st.error(
                        f"❌ Question {question_number}: Incorrect"
                    )

                    st.write(
                        f"**Your answer:** "
                        f"{selected_answer}"
                    )

                    st.write(
                        f"**Correct answer:** "
                        f"{correct_answer}. {correct_text}"
                    )

                st.write(
                    f"**Q{question_number}. "
                    f"{question_text}**"
                )

                st.divider()


            # =================================================
            # RETRY QUIZ
            # =================================================

            if st.button(
                "🔄 Generate New Quiz"
            ):

                st.session_state.quiz_questions = []

                st.session_state.quiz_answers = {}

                st.session_state.quiz_submitted = False

                st.session_state.quiz_score = 0

                st.rerun()