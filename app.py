import tempfile
import streamlit as st

from main import (
    create_vector_db,
    read_txt,
    read_pdf,
    read_docx,
    process_website,
    generate_objective_questions,
    generate_subjective_questions,
    evaluate_objective,
    evaluate_subjective,
    generate_feedback,
    ask_ai
)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Assessment & RAG System",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================
st.title("📘 AI Assessment & RAG System")

# ==========================================
# SESSION STATE
# ==========================================
if "objective_questions" not in st.session_state:
    st.session_state.objective_questions = []

if "subjective_questions" not in st.session_state:
    st.session_state.subjective_questions = []

if "generated_objective_preview" not in st.session_state:
    st.session_state.generated_objective_preview = []

if "generated_subjective_preview" not in st.session_state:
    st.session_state.generated_subjective_preview = []

# ==========================================
# SIDEBAR
# ==========================================
menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Upload Materials",
        "Generate Assessment",
        "Take Assessment",
        "AI Chatbot"
    ]
)

# ==========================================
# UPLOAD MATERIALS
# ==========================================
if menu == "Upload Materials":

    st.header("📂 Upload Learning Material")

    upload_type = st.radio(
        "Choose Upload Type",
        ["File Upload", "Link Upload"]
    )

    # FILE UPLOAD
    if upload_type == "File Upload":

        uploaded_file = st.file_uploader(
            "Upload PDF/TXT/DOCX",
            type=["pdf", "txt", "docx"]
        )

        if uploaded_file:

            suffix = uploaded_file.name.split(".")[-1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{suffix}"
            ) as tmp:

                tmp.write(uploaded_file.read())

                file_path = tmp.name

            text = ""

            if suffix == "txt":
                text = read_txt(file_path)

            elif suffix == "pdf":
                text = read_pdf(file_path)

            elif suffix == "docx":
                text = read_docx(file_path)

            create_vector_db([text])

            st.success(
                "File uploaded and indexed successfully"
            )

    # WEBSITE LINK
    else:

        website_url = st.text_input(
            "Enter Website URL"
        )

        if st.button("Process Link"):

            text = process_website(
                website_url
            )

            create_vector_db([text])

            st.success(
                "Website content processed"
            )

# ==========================================
# GENERATE ASSESSMENT
# ==========================================
elif menu == "Generate Assessment":

    st.header("📝 Generate Assessment")

    assessment_type = st.radio(
        "Choose Assessment Type",
        [
            "Objective",
            "Subjective"
        ]
    )

    # ==========================================
    # OBJECTIVE PREVIEW
    # ==========================================
    if assessment_type == "Objective":

        topic = st.text_input(
            "Enter Topic",
            key="gen_obj_topic"
        )

        num_questions = st.slider(
            "Number of Questions",
            5,
            15,
            10,
            key="gen_obj_slider"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Generate Objective Questions"
            ):

                st.session_state.generated_objective_preview = (
                    generate_objective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Generated"
                )

        with col2:

            if st.button(
                "🔄 Change Questions"
            ):

                st.session_state.generated_objective_preview = (
                    generate_objective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Changed"
                )

        if len(
            st.session_state.generated_objective_preview
        ) > 0:

            st.subheader(
                "📋 Sample Objective Questions"
            )

            for i, q in enumerate(
                st.session_state.generated_objective_preview,
                start=1
            ):

                st.write(
                    f"### Q{i}. {q['question']}"
                )

                for option in q["options"]:

                    st.write(f"- {option}")

                st.divider()

    # ==========================================
    # SUBJECTIVE PREVIEW
    # ==========================================
    else:

        topic = st.text_input(
            "Enter Topic",
            key="gen_sub_topic"
        )

        num_questions = st.slider(
            "Number of Questions",
            5,
            15,
            10,
            key="gen_sub_slider"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Generate Subjective Questions"
            ):

                st.session_state.generated_subjective_preview = (
                    generate_subjective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Generated"
                )

        with col2:

            if st.button(
                "🔄 Change Questions"
            ):

                st.session_state.generated_subjective_preview = (
                    generate_subjective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Changed"
                )

        if len(
            st.session_state.generated_subjective_preview
        ) > 0:

            st.subheader(
                "📋 Sample Subjective Questions"
            )

            for i, q in enumerate(
                st.session_state.generated_subjective_preview,
                start=1
            ):

                st.write(f"### Q{i}. {q}")

                st.divider()

# ==========================================
# TAKE ASSESSMENT
# ==========================================
elif menu == "Take Assessment":

    st.header("🧠 Take Assessment")

    mode = st.radio(
        "Choose Mode",
        ["Objective", "Subjective"]
    )

    # ==========================================
    # OBJECTIVE TEST
    # ==========================================
    if mode == "Objective":

        st.subheader("Objective Test Setup")

        topic = st.text_input(
            "Enter Topic",
            key="obj_topic"
        )

        num_questions = st.slider(
            "Number of Questions",
            5,
            15,
            10,
            key="obj_slider"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Generate MCQs"):

                st.session_state.objective_questions = (
                    generate_objective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success("MCQs Generated")

        with col2:

            if st.button("🔄 Change Questions"):

                st.session_state.objective_questions = (
                    generate_objective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success("Questions Changed")

        if len(st.session_state.objective_questions) > 0:

            st.subheader("📝 Objective Assessment")

            user_answers = []

            for i, q in enumerate(
                st.session_state.objective_questions
            ):

                answer = st.radio(
                    q["question"],
                    q["options"],
                    key=f"mcq_{i}"
                )

                user_answers.append(answer)

            if st.button("Submit Test"):

                score = evaluate_objective(
                    user_answers,
                    st.session_state.objective_questions
                )

                st.success(
                    f"Score: {score}/{len(st.session_state.objective_questions)}"
                )

                feedback = generate_feedback(score)

                st.subheader("📊 Feedback")

                st.write(
                    "Performance:",
                    feedback["performance"]
                )

                for item in feedback["feedback"]:

                    st.write(f"• {item}")

    # ==========================================
    # SUBJECTIVE TEST
    # ==========================================
    else:

        st.subheader("Subjective Test Setup")

        topic = st.text_input(
            "Enter Topic",
            key="sub_topic"
        )

        num_questions = st.slider(
            "Number of Questions",
            5,
            15,
            10,
            key="sub_slider"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Generate Subjective Questions"
            ):

                st.session_state.subjective_questions = (
                    generate_subjective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Generated"
                )

        with col2:

            if st.button(
                "🔄 Change Questions"
            ):

                st.session_state.subjective_questions = (
                    generate_subjective_questions(
                        topic,
                        num_questions
                    )
                )

                st.success(
                    "Questions Changed"
                )

        if len(st.session_state.subjective_questions) > 0:

            answers = []

            for i, q in enumerate(
                st.session_state.subjective_questions
            ):

                ans = st.text_area(
                    q,
                    key=f"sub_{i}"
                )

                answers.append(ans)

            if st.button(
                "Submit Subjective Test"
            ):

                st.subheader(
                    "📊 AI Evaluation"
                )

                for q, ans in zip(
                    st.session_state.subjective_questions,
                    answers
                ):

                    result = evaluate_subjective(
                        q,
                        ans
                    )

                    st.write("### Question")
                    st.write(q)

                    st.write("### Evaluation")
                    st.write(result)

                    st.divider()

# ==========================================
# AI CHATBOT
# ==========================================
elif menu == "AI Chatbot":

    st.header("🤖 AI Academic Chatbot")

    question = st.text_input(
        "Ask a Question"
    )

    if st.button(
        "Ask AI"
    ):

        response = ask_ai(question)

        st.subheader(
            "AI Response"
        )

        st.write(response)