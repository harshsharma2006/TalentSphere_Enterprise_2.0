"""
TalentSphere Enterprise 2.0 - Students Module
Handles College Admin Student Directory, College Student Portal, and High School Student Career Guidance.
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, profile_card, empty_state
from services.student_service import StudentService
from services.report_service import ReportService
from ai_engine.career_recommender import CareerRecommender
from core.permissions import Role

def render_students_module(current_user: dict):
    role = current_user.get("role")
    if role in [Role.SUPER_ADMIN.value, Role.COLLEGE_ADMIN.value]:
        render_college_admin_portal(current_user)
    elif role == Role.COLLEGE_STUDENT.value:
        render_college_student_portal(current_user)
    elif role == Role.HIGH_SCHOOL_STUDENT.value:
        render_high_school_student_portal(current_user)
    else:
        render_college_admin_portal(current_user)

def render_college_admin_portal(current_user: dict):
    page_header("Academic & Placement Administration", "Monitor student academic progress, skill readiness, and placement outcomes.", "College Admin", "yellow")

    students = StudentService.get_all_students()
    depts = StudentService.get_academic_departments()

    stat_row([
        {"title": "Total Students", "value": len(students), "subtitle": "Enrolled learners", "icon": "users", "color": THEME["primary"]},
        {"title": "Academic Depts", "value": len(depts), "subtitle": "Engineering, CS, Business", "icon": "graduation_cap", "color": THEME["dark_blue"]},
        {"title": "Avg Readiness", "value": f"{round(sum([s['placement_readiness_score'] for s in students])/max(len(students),1), 1)}%", "subtitle": "Campus placement index", "icon": "award", "color": THEME["success"]},
        {"title": "Placed / Offers", "value": len([s for s in students if s['placement_status'] == 'PLACED']), "subtitle": "Graduates placed", "icon": "briefcase", "color": THEME["warning"]},
    ])

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Student Directory", "Placement Reports & PDF"])

    with tab1:
        st.subheader("Campus Student Records")
        if students:
            df = pd.DataFrame(students)
            cols = ["student_id_number", "full_name", "department", "degree_program", "current_year", "gpa", "placement_readiness_score", "placement_status"]
            avail = [c for c in cols if c in df.columns]

            # Filter
            search = st.text_input("Search student by ID, Name or Department", key="std_search")
            if search:
                term = search.lower()
                df = df[df["full_name"].str.lower().str.contains(term) | df["student_id_number"].str.lower().str.contains(term) | df["department"].str.lower().str.contains(term)]

            st.dataframe(df[avail], use_container_width=True, hide_index=True)
        else:
            empty_state("No Students Enrolled", "Import or register student records.")

    with tab2:
        st.subheader("Placement Readiness PDF Generation")
        st.write("Generate official placement intelligence reports for corporate recruiters and accreditation boards.")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            if st.button("Generate Placement Readiness PDF", use_container_width=True):
                pdf_bytes = ReportService.generate_students_placement_pdf(students)
                st.download_button(
                    label="⬇️ Download Placement PDF",
                    data=pdf_bytes,
                    file_name="TalentSphere_Placement_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with col_p2:
            csv_str = ReportService.export_csv(students)
            st.download_button(
                label="⬇️ Export Student Data to CSV",
                data=csv_str,
                file_name="TalentSphere_Students.csv",
                mime="text/csv",
                use_container_width=True
            )

def render_college_student_portal(current_user: dict):
    page_header("College Student Career Launchpad", "Track academic progress, build ATS resumes, and accelerate placement readiness.", "College Student", "blue")

    student = StudentService.get_student_by_user_id(current_user["id"])
    readiness = student.get("placement_readiness_score", 75.0) if student else 75.0

    profile_card(
        name=f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}".strip() or current_user.get("username"),
        role_title=f"{student.get('degree_program', 'B.S. Computer Science')} (Year {student.get('current_year', 3)})" if student else "College Student",
        email=current_user.get("email"),
        org_name=student.get("department", "Computer Science & Engineering") if student else "Engineering Campus",
        stats=[
            {"label": "Student ID", "val": student.get("student_id_number", "STU-2026-001") if student else "STU-001"},
            {"label": "GPA", "val": f"{student.get('gpa', 3.85):.2f}" if student else "3.85"},
            {"label": "Readiness", "val": f"{readiness}%"}
        ]
    )

    tab1, tab2 = st.tabs(["Placement Readiness Radar", "Recommended Career Tracks"])

    with tab1:
        st.subheader("Placement Preparedness Analytics")
        st.write("Your placement score is evaluated continuously based on technical assessments, coding practice, and ATS resume quality.")
        st.progress(readiness / 100.0)

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            metric_card("Technical Aptitude", "88%", "Data Structures & Algos", "cpu", THEME["primary"])
        with col_m2:
            metric_card("ATS Resume Hygiene", "85%", "Verified keyword match", "file_text", THEME["success"])
        with col_m3:
            metric_card("Mock Interviews", "82%", "STAR communication score", "users", THEME["dark_blue"])

    with tab2:
        st.subheader("Target Industry Roles")
        user_skills = ["Python", "FastAPI", "React", "SQL", "Git", "Docker"]
        recs = CareerRecommender.recommend_roles(user_skills)
        for r in recs[:3]:
            st.markdown(f"""
            <div class="ts-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: {THEME['dark_blue']};">{r['role']}</h4>
                    <span class="ts-badge ts-badge-blue">{r['match_percentage']}% Fit</span>
                </div>
                <p style="color: {THEME['secondary']}; font-size: 0.9rem; margin: 0.4rem 0;">{r['description']}</p>
                <div style="font-size: 0.85rem;"><strong>Matched Skills:</strong> {', '.join(r['matched_skills'])}</div>
                <div style="font-size: 0.85rem; color: {THEME['danger']};"><strong>Skills to Learn:</strong> {', '.join(r['missing_skills'][:4])}</div>
            </div>
            """, unsafe_allow_html=True)

def render_high_school_student_portal(current_user: dict):
    page_header("High School Future Pathways Explorer", "Discover your core interests, RIASEC career profiles, and foundational skills.", "High School Student", "yellow")

    profile_card(
        name=f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}".strip() or current_user.get("username"),
        role_title="High School Junior / Senior (Grade 11-12)",
        email=current_user.get("email"),
        org_name="Pre-College STEM Academy"
    )

    st.subheader("Holland Code (RIASEC) Career Exploration")
    st.write("Select the activities that excite you most to generate personalized degree and vocational recommendations:")

    with st.form("riasec_form"):
        col1, col2 = st.columns(2)
        with col1:
            q1 = st.checkbox("I enjoy building physical models, electronics, or robotics.")
            q2 = st.checkbox("I love solving complex math puzzles and conducting science experiments.")
            q3 = st.checkbox("I express myself creatively through digital design, writing, or art.")
        with col2:
            q4 = st.checkbox("I like helping and tutoring others to solve personal or academic challenges.")
            q5 = st.checkbox("I enjoy leading school clubs, organizing events, or pitching startup ideas.")
            q6 = st.checkbox("I prefer working with structured schedules, organized tables, and clear rules.")

        submitted = st.form_submit_button("Analyze My Career Profile", use_container_width=True)

    if submitted:
        traits = []
        if q1: traits.append("Realistic")
        if q2: traits.append("Investigative")
        if q3: traits.append("Artistic")
        if q4: traits.append("Social")
        if q5: traits.append("Enterprising")
        if q6: traits.append("Conventional")

        if not traits:
            traits = ["Investigative", "Enterprising"]

        st.success(f"Primary Personality Archetypes: {', '.join(traits)}")
        st.markdown("### Top Recommended Pre-College Career Fields:")
        recs = CareerRecommender.recommend_roles(user_skills=["Python", "Math"], riasec_traits=traits)
        for r in recs[:3]:
            st.markdown(f"""
            <div class="ts-card">
                <h4 style="margin: 0; color: {THEME['primary']};">{r['role']} ({r['category']})</h4>
                <p style="font-size: 0.9rem; color: {THEME['secondary']}; margin: 0.4rem 0;">{r['description']}</p>
                <div style="font-size: 0.85rem;"><strong>Recommended Degree Majors:</strong> Computer Science, Electrical Engineering, Cognitive Science</div>
            </div>
            """, unsafe_allow_html=True)
