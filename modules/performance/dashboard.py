"""
TalentSphere Enterprise 2.0 - Performance & Goals Module
Reviews management, KPI tracking, and rating distribution.
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.performance_service import PerformanceService
from services.employee_service import EmployeeService
from core.permissions import Role

def render_performance_module(current_user: dict):
    page_header("Enterprise Performance & KPI Reviews", "Conduct reviews, track quarterly milestones, and analyze organizational talent distribution.", "Performance", "blue")

    is_manager = current_user.get("role") in [Role.SUPER_ADMIN.value, Role.HR_ADMIN.value]
    reviews = PerformanceService.get_all_reviews()

    stat_row([
        {"title": "Total Reviews", "value": len(reviews), "subtitle": "Evaluations recorded", "icon": "award", "color": THEME["primary"]},
        {"title": "Avg Org Score", "value": f"{round(sum([r['overall_score'] for r in reviews])/max(len(reviews),1), 1)} / 5.0", "subtitle": "Workforce rating", "icon": "compass", "color": THEME["success"]},
        {"title": "Completed Cycles", "value": len([r for r in reviews if r['status'] == 'COMPLETED']), "subtitle": "Finalized reviews", "icon": "shield_check", "color": THEME["dark_blue"]},
        {"title": "Top Performers", "value": len([r for r in reviews if r['overall_score'] >= 4.5]), "subtitle": "Exceeding expectations", "icon": "users", "color": THEME["warning"]},
    ])

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Performance History", "Conduct New Review" if is_manager else "My Goals"])

    with tab1:
        st.subheader("Performance Evaluations Log")
        if reviews:
            df = pd.DataFrame(reviews)
            cols = ["id", "employee_name", "reviewer_name", "review_cycle", "overall_score", "status", "created_at"]
            avail = [c for c in cols if c in df.columns]
            st.dataframe(df[avail], use_container_width=True, hide_index=True)
        else:
            empty_state("No Evaluations Recorded", "Completed performance evaluations will appear here.")

    with tab2:
        if is_manager:
            st.subheader("Record Employee Evaluation")
            employees = EmployeeService.get_all_employees()

            with st.form("create_review_form"):
                col1, col2 = st.columns(2)
                with col1:
                    emp_id = st.selectbox(
                        "Employee Under Review*",
                        options=[e["id"] for e in employees] if employees else [0],
                        format_func=lambda eid: f"{[e['full_name'] for e in employees if e['id'] == eid][0]} ({[e['designation'] for e in employees if e['id'] == eid][0]})" if employees else "No employees"
                    )
                    cycle = st.selectbox("Review Cycle*", ["2026 Q1 Review", "2026 Q2 Review", "2026 Mid-Year Evaluation", "2026 Annual Review"])
                with col2:
                    score = st.slider("Overall Performance Score (1.0 to 5.0)*", 1.0, 5.0, 4.0, step=0.1)

                feedback = st.text_area("Manager Executive Feedback*", "Strong technical leadership and high delivery velocity on critical project milestones.")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    strengths = st.text_input("Key Strengths", "System architecture, mentor to juniors, clean code")
                with col_s2:
                    improvements = st.text_input("Areas for Development", "Delegation on multi-team epics")

                submit = st.form_submit_button("Submit Performance Review", use_container_width=True)
                if submit:
                    if not employees:
                        st.error("No employee records available.")
                    else:
                        PerformanceService.create_review(
                            employee_id=emp_id,
                            reviewer_id=current_user["id"],
                            review_cycle=cycle,
                            overall_score=score,
                            manager_feedback=feedback,
                            strengths=strengths,
                            areas_for_improvement=improvements
                        )
                        st.success("Performance review submitted and finalized successfully!")
                        st.rerun()
        else:
            st.subheader("My Assigned Goals")
            emp = EmployeeService.get_employee_by_user_id(current_user["id"])
            emp_id = emp["id"] if emp else 1
            goals = PerformanceService.get_employee_goals(emp_id)
            if goals:
                for g in goals:
                    st.write(f"**{g['title']}** - Progress: {g['progress_percentage']}%")
                    st.progress(g['progress_percentage'] / 100.0)
            else:
                empty_state("No Goals Assigned", "Connect with your manager to establish quarterly goals.")
