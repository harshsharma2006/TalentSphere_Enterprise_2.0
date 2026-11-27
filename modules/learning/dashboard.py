"""
TalentSphere Enterprise 2.0 - Learning & Upskilling Module
Course Catalog, Self-Paced Enrollments, and Certifications.
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.learning_service import LearningService

def render_learning_module(current_user: dict):
    page_header("Enterprise Learning & Upskilling Academy", "Access curated corporate coursework, bridge skill gaps, and earn recognized certifications.", "Learning", "blue")

    courses = LearningService.get_all_courses()
    enrollments = LearningService.get_user_enrollments(current_user["id"])

    stat_row([
        {"title": "Available Courses", "value": len(courses), "subtitle": "Catalog offerings", "icon": "book_open", "color": THEME["primary"]},
        {"title": "My Enrollments", "value": len(enrollments), "subtitle": "Active courses", "icon": "award", "color": THEME["dark_blue"]},
        {"title": "Completed", "value": len([e for e in enrollments if e["status"] == "COMPLETED"]), "subtitle": "Earned certifications", "icon": "shield_check", "color": THEME["success"]},
        {"title": "In Progress", "value": len([e for e in enrollments if e["status"] != "COMPLETED"]), "subtitle": "Ongoing modules", "icon": "clock", "color": THEME["warning"]},
    ])

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Course Catalog", "My Learning Dashboard"])

    with tab1:
        st.subheader("Enterprise Catalog")
        category_filter = st.selectbox("Filter by Category", ["All", "Software Engineering", "Cloud & DevOps", "Data & AI", "Leadership & Management"])
        
        filtered_courses = courses if category_filter == "All" else [c for c in courses if c["category"] == category_filter]
        
        for c in filtered_courses:
            with st.container():
                st.markdown(f"""
                <div class="ts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: {THEME['dark_blue']};">{c['title']}</h4>
                        <span class="ts-badge ts-badge-blue">{c['level']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: {THEME['secondary']}; margin: 0.25rem 0;">
                        Provider: {c['provider']} • Duration: {c['duration_hours']} Hours • Category: {c['category']}
                    </div>
                    <p style="font-size: 0.9rem; margin: 0.5rem 0;">{c['description']}</p>
                    <div style="font-size: 0.8rem; color: {THEME['primary']};">
                        <strong>Skill Tags:</strong> {', '.join(c.get('skill_tags', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Enroll in {c['title']}", key=f"enroll_btn_{c['id']}"):
                    res = LearningService.enroll_user(current_user["id"], c["id"])
                    if res.get("already_enrolled"):
                        st.info("You are already enrolled in this course!")
                    else:
                        st.success("Enrolled successfully! Head to 'My Learning Dashboard' to begin.")
                        st.rerun()

    with tab2:
        st.subheader("My Enrolled Courses")
        if enrollments:
            for e in enrollments:
                st.markdown(f"""
                <div class="ts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{e['course_title']}</h4>
                        <span class="ts-badge {'ts-badge-green' if e['status'] == 'COMPLETED' else 'ts-badge-blue'}">{e['status']}</span>
                    </div>
                    <p style="font-size: 0.85rem; color: {THEME['secondary']}; margin: 0.35rem 0;">{e['category']} • {e['duration_hours']} Hours</p>
                </div>
                """, unsafe_allow_html=True)
                new_val = st.slider(f"Progress for '{e['course_title']}'", 0, 100, e["progress_percentage"], key=f"prog_{e['id']}")
                if new_val != e["progress_percentage"]:
                    LearningService.update_progress(e["id"], new_val)
                    st.success("Progress saved!")
                    st.rerun()
        else:
            empty_state("No Active Enrollments", "Browse the course catalog above to enroll.")
