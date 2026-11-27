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
from ai_engine.ai_mentor import AICareerMentor

def render_career_module(current_user: dict):
    page_header("Career Pathways & AI Coaching", "Explore career trajectories, assess competency gaps, and receive structured mentoring roadmaps.", "Career Growth", "blue")

    paths = CareerService.get_all_career_paths()

    tab1, tab2, tab3, tab4 = st.tabs(["Career Trajectories", "Skill Gap Diagnostics", "90-Day Growth Blueprint", "🤖 AI Career Advisor & Mentor"])

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

    with tab4:
        st.subheader("🤖 AI Interactive Career Advisory Mentor")
        st.write("Receive strategic mentorship on engineering transitions, system design interviews, certifications, and executive promotion roadmaps.")

        st.markdown("**Quick Advisory Topics:**")
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("🚀 Roadmap to Cloud & DevOps", use_container_width=True):
                st.session_state["mentor_query"] = "How do I become a Senior Cloud and DevOps Engineer?"
            if st.button("🧠 Transition to AI / MLOps", use_container_width=True):
                st.session_state["mentor_query"] = "What is the best roadmap to transition into AI and MLOps engineering?"
        with col_q2:
            if st.button("🎯 Mastering STAR Interviews", use_container_width=True):
                st.session_state["mentor_query"] = "How should I structure behavioral and system design interview answers using STAR?"
            if st.button("📈 Promotion & Salary Strategy", use_container_width=True):
                st.session_state["mentor_query"] = "How do I maximize my promotion velocity and salary leveling?"

        user_q = st.text_input(
            "Ask AI Career Mentor a Custom Question",
            value=st.session_state.get("mentor_query", "How do I prepare for a Senior Backend System Design interview?"),
            key="mentor_text_input"
        )

        if st.button("Consult AI Mentor", type="primary", use_container_width=True):
            st.session_state["mentor_advice"] = AICareerMentor.get_advice(user_q)

        if "mentor_advice" in st.session_state:
            advice = st.session_state["mentor_advice"]
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            formatted_guidance = advice['guidance'].replace("\n", "<br>")
            st.markdown(f"""
            <div class="ts-card" style="border-left: 4px solid #2563EB;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h3 style="margin: 0; color: {THEME['dark_blue']};">{advice['title']}</h3>
                    <span class="ts-badge ts-badge-blue">{advice['category']}</span>
                </div>
                <div style="font-size: 0.95rem; line-height: 1.7; color: #1E293B;">
                    {formatted_guidance}
                </div>
            </div>
            """, unsafe_allow_html=True)
