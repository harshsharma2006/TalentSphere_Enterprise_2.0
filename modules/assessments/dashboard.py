"""
TalentSphere Enterprise 2.0 - Technical & Aptitude Assessments Module
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.student_service import StudentService
from core.permissions import Role

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
