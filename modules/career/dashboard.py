"""
TalentSphere Enterprise 2.0 - Career Pathways & AI Coaching Module
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.career_service import CareerService
from ai_engine.career_recommender import CareerRecommender
from ai_engine.skill_analyzer import SkillAnalyzer
from ai_engine.ai_coach import AICareerCoach

def render_career_module(current_user: dict):
    page_header("Career Pathways & AI Coaching", "Explore career trajectories, assess competency gaps, and receive structured mentoring roadmaps.", "Career Growth", "blue")

    paths = CareerService.get_all_career_paths()

    tab1, tab2, tab3 = st.tabs(["Career Trajectories", "Skill Gap Diagnostics", "AI Career Coach"])

    with tab1:
        st.subheader("Enterprise Career Paths")
        if paths:
            for p in paths:
                st.markdown(f"""
                <div class="ts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: {THEME['dark_blue']};">{p['current_role']} ➔ {p['target_role']}</h4>
                        <span class="ts-badge ts-badge-blue">{p['typical_timeline_months']} Months</span>
                    </div>
                    <div style="font-size: 0.85rem; color: {THEME['secondary']}; margin: 0.3rem 0;">Department: {p['department']}</div>
                    <p style="font-size: 0.9rem; margin: 0.4rem 0;">{p['description']}</p>
                    <div style="font-size: 0.8rem; color: {THEME['primary']};">
                        <strong>Required Skills:</strong> {', '.join(p.get('required_skills', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("No Paths Defined", "Career trajectories will be loaded here.")

    with tab2:
        st.subheader("Competency Gap Diagnostic")
        col1, col2 = st.columns(2)
        with col1:
            my_skills_raw = st.text_area("Your Current Competencies (comma separated)", "Python, FastAPI, SQL, Git, Linux")
        with col2:
            target_role = st.selectbox("Target Career Role", [
                "Senior Cloud & DevOps Engineer (AWS, Kubernetes, Terraform, Docker, Python)",
                "Staff Full-Stack Architect (React, Node.js, Python, PostgreSQL, System Design)",
                "Lead AI / ML Engineer (Python, PyTorch, Scikit-learn, MLOps, Deep Learning)"
            ])

        if st.button("Run Skill Gap Analysis", use_container_width=True):
            my_skills = [s.strip() for s in my_skills_raw.split(",") if s.strip()]
            role_title = target_role.split("(")[0].strip()
            skills_in_parens = target_role.split("(")[1].replace(")", "")
            target_skills = [s.strip() for s in skills_in_parens.split(",") if s.strip()]

            analysis = SkillAnalyzer.analyze_skill_gap(my_skills, target_skills)
            st.session_state["skill_gap_result"] = analysis
            st.session_state["target_role_name"] = role_title

        if "skill_gap_result" in st.session_state:
            res = st.session_state["skill_gap_result"]
            st.markdown(f"""
            <div class="ts-card" style="border-left: 4px solid {THEME['primary']};">
                <h3>Readiness Fit: {res['readiness_percentage']}%</h3>
                <p><strong>Matched Skills:</strong> {', '.join(res['matched_skills']) if res['matched_skills'] else 'None'}</p>
                <p style="color: {THEME['danger']};"><strong>Missing Skills:</strong> {', '.join(res['missing_skills']) if res['missing_skills'] else 'Fully Qualified!'}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("90-Day AI Career Growth Blueprint")
        st.write("Generates milestone-driven action plans tailored to your targeted promotion or career transition.")
        target_role_input = st.text_input("Target Promotion Role", "Senior DevOps Engineer")
        gap_skills_input = st.text_input("Priority Missing Skills to Master", "Kubernetes, Terraform, AWS")

        if st.button("Generate 90-Day Growth Blueprint", use_container_width=True):
            missing_list = [s.strip() for s in gap_skills_input.split(",") if s.strip()]
            growth_plan = AICareerCoach.generate_growth_plan(target_role_input, missing_list)
            for item in growth_plan:
                st.markdown(f"""
                <div class="ts-card">
                    <h4 style="margin: 0; color: {THEME['primary']};">{item['phase']} — {item['focus']}</h4>
                    <ul style="margin-top: 0.5rem; margin-bottom: 0;">
                        {''.join([f'<li>{act}</li>' for act in item['actions']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
