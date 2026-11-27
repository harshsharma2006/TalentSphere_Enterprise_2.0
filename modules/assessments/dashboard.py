"""
TalentSphere Enterprise 2.0 - Technical & Aptitude Assessments Module
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.student_service import StudentService
from core.permissions import Role
from ai_engine.interview_simulator import InterviewSimulator

SAMPLE_ASSESSMENTS = [
    {
        "id": 1,
        "title": "Data Structures & Algorithmic Complexity",
        "category": "Computer Science",
        "questions": [
            {
                "q": "What is the average time complexity of searching in an optimized Balanced Binary Search Tree (AVL / Red-Black)?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "ans": "O(log n)"
            },
            {
                "q": "Which data structure operates on a First-In, First-Out (FIFO) access order?",
                "options": ["Stack", "Queue", "Heap", "Hash Table"],
                "ans": "Queue"
            },
            {
                "q": "Which sorting algorithm achieves worst-case O(n log n) performance with O(1) auxiliary space?",
                "options": ["Merge Sort", "Quick Sort", "Heap Sort", "Bubble Sort"],
                "ans": "Heap Sort"
            }
        ]
    },
    {
        "id": 2,
        "title": "Quantitative & Logical Reasoning",
        "category": "Aptitude",
        "questions": [
            {
                "q": "If a train travels 360 km at 90 km/h, how many hours does the journey take?",
                "options": ["3 hours", "4 hours", "4.5 hours", "5 hours"],
                "ans": "4 hours"
            },
            {
                "q": "Find the next number in the sequence: 2, 6, 12, 20, 30, ?",
                "options": ["40", "42", "44", "46"],
                "ans": "42"
            }
        ]
    }
]

def render_assessments_module(current_user: dict):
    page_header("Skills & Placement Assessment Center", "Benchmark technical fundamentals, quantitative aptitude, and problem-solving readiness.", "Assessments", "blue")

    tab_std, tab_mock = st.tabs(["📝 Multiple Choice Assessments", "🎯 AI Interactive Mock Interview Simulator"])

    with tab_std:
        stat_row([
            {"title": "Available Tests", "value": len(SAMPLE_ASSESSMENTS), "subtitle": "Core disciplines", "icon": "cpu", "color": THEME["primary"]},
            {"title": "Passing Benchmark", "value": "75%", "subtitle": "Enterprise standard", "icon": "award", "color": THEME["success"]},
            {"title": "Placement Weight", "value": "35%", "subtitle": "Campus scorecard", "icon": "graduation_cap", "color": THEME["dark_blue"]},
        ])

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        selected_test = st.selectbox("Select Assessment Test", options=SAMPLE_ASSESSMENTS, format_func=lambda t: f"{t['title']} ({t['category']})")

        st.subheader(f"Test: {selected_test['title']}")
        with st.form(f"assessment_form_{selected_test['id']}"):
            user_answers = {}
            for idx, q_item in enumerate(selected_test["questions"]):
                st.markdown(f"**Q{idx+1}: {q_item['q']}**")
                user_answers[idx] = st.radio(f"Options for Q{idx+1}", q_item["options"], key=f"q_{selected_test['id']}_{idx}", label_visibility="collapsed")
                st.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)

            submitted = st.form_submit_button("Submit Assessment & Calculate Score", use_container_width=True)

        if submitted:
            correct = 0
            total = len(selected_test["questions"])
            for idx, q_item in enumerate(selected_test["questions"]):
                if user_answers.get(idx) == q_item["ans"]:
                    correct += 1

            score_percent = round((correct / total) * 100, 1)
            if score_percent >= 70:
                st.success(f"🎉 Assessment Passed! Score: {score_percent}% ({correct}/{total} correct)")
            else:
                st.warning(f"Assessment Completed. Score: {score_percent}% ({correct}/{total} correct). Keep practicing!")

            # Update student placement score if student user
            if current_user.get("role") in [Role.COLLEGE_STUDENT.value, Role.HIGH_SCHOOL_STUDENT.value]:
                std = StudentService.get_student_by_user_id(current_user["id"])
                if std:
                    StudentService.update_placement_score(std["id"], score_percent)
                    st.info("Your updated placement readiness score has been persisted to your campus record!")

    with tab_mock:
        st.subheader("🎯 Enterprise AI Mock Interview Simulator")
        st.write("Rehearse real-world technical and behavioral interview questions with real-time AI scoring across key concept coverage, the STAR framework, and answer depth.")

        roles = InterviewSimulator.get_roles()
        selected_role = st.selectbox("Select Interview Track / Role", roles)

        questions = InterviewSimulator.get_questions_for_role(selected_role)
        selected_q = st.selectbox(
            "Select Question",
            questions,
            format_func=lambda q: f"[{q['type']}] {q['question']}"
        )

        st.markdown(f"""
        <div class="ts-card" style="border-left: 4px solid {THEME['primary']}; margin-top: 0.5rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="ts-badge ts-badge-blue">{selected_q['type']}</span>
                <span style="font-size: 0.85rem; color: #64748B;">Core Concepts Expected: {len(selected_q['expected_concepts'])}</span>
            </div>
            <h4 style="margin: 0; color: {THEME['dark_blue']}; line-height: 1.5;">{selected_q['question']}</h4>
        </div>
        """, unsafe_allow_html=True)

        candidate_answer = st.text_area(
            "Your Detailed Interview Response",
            "In our system, we deployed a Redis cluster to cache high-frequency requests with TTL invalidation. To prevent cache stampedes, we implemented write-through caching with background workers, reducing database load by 60%.",
            height=140,
            help="Structure your response following the STAR framework: Situation, Task, Action, and Quantified Result."
        )

        if st.button("🤖 Evaluate My Answer with AI", type="primary", use_container_width=True):
            st.session_state["interview_eval"] = InterviewSimulator.evaluate_response(selected_q, candidate_answer)

        if "interview_eval" in st.session_state:
            ev = st.session_state["interview_eval"]
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

            score_color = THEME["success"] if ev["overall_score"] >= 75 else THEME["warning"]
            stat_row([
                {"title": "Interview Match Score", "value": f"{ev['overall_score']}%", "subtitle": "Composite rating", "icon": "award", "color": score_color},
                {"title": "Concept Coverage", "value": f"{ev['concept_coverage_pct']}%", "subtitle": f"{len(ev['matched_concepts'])} concepts matched", "icon": "cpu", "color": THEME["primary"]},
                {"title": "STAR Adherence", "value": f"{int(ev['star_score'])}%", "subtitle": "Structure compliance", "icon": "check_circle", "color": THEME["dark_blue"]},
                {"title": "Response Depth", "value": f"{ev['word_count']} words", "subtitle": "Detail & completeness", "icon": "file_text", "color": THEME["secondary"]}
            ])

            col_mc1, col_mc2 = st.columns(2)
            with col_mc1:
                matched_badges = " ".join([f"<span class='ts-badge ts-badge-green'>{c}</span>" for c in ev['matched_concepts']]) if ev['matched_concepts'] else "<em>None detected</em>"
                st.markdown(f"""
                <div class="ts-card" style="border-top: 4px solid #16A34A !important;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #15803D !important; font-weight: 700;">Matched Technical Concepts</h4>
                    <div>{matched_badges}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_mc2:
                missing_badges = " ".join([f"<span class='ts-badge ts-badge-orange'>{c}</span>" for c in ev['missing_concepts']]) if ev['missing_concepts'] else "<em>All concepts mastered!</em>"
                st.markdown(f"""
                <div class="ts-card" style="border-top: 4px solid #EA580C !important;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #C2410C !important; font-weight: 700;">Suggested Concepts to Mention</h4>
                    <div>{missing_badges}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 🎯 AI Evaluation Feedback")
            for fb in ev["feedback"]:
                st.info(f"💡 {fb}")

            with st.expander("🌟 View Ideal Senior Architect Model Answer"):
                st.markdown(f"""
                <div style="background: #F1F5F9; border-radius: 6px; padding: 1rem; color: #0F172A; line-height: 1.6; font-size: 0.95rem;">
                    {ev['model_answer']}
                </div>
                """, unsafe_allow_html=True)
