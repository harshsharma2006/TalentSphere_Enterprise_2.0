"""
TalentSphere Enterprise 2.0 - Recruitment & Pipeline Module
Job Requisitions, Candidate Applications, Pipeline Management, AI Match Scoring, and Requisition Generation.
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from services.recruitment_service import RecruitmentService
from core.permissions import Role
from ai_engine.job_generator import JobRequisitionGenerator

def render_recruitment_module(current_user: dict):
    is_recruiter = current_user.get("role") in [Role.SUPER_ADMIN.value, Role.HR_ADMIN.value]

    if is_recruiter:
        render_recruiter_view(current_user)
    else:
        render_candidate_job_board(current_user)

def render_recruiter_view(current_user: dict):
    page_header("Recruitment & Talent Acquisition Hub", "Create requisitions, screen applicants with AI match ranking, and schedule interviews.", "HR Admin", "blue")

    jobs = RecruitmentService.get_all_jobs()
    apps = RecruitmentService.get_applications()

    stat_row([
        {"title": "Open Positions", "value": len([j for j in jobs if j["status"] == "OPEN"]), "subtitle": "Active requisitions", "icon": "briefcase", "color": THEME["primary"]},
        {"title": "Total Candidates", "value": len(apps), "subtitle": "Applications received", "icon": "users", "color": THEME["dark_blue"]},
        {"title": "Under Review", "value": len([a for a in apps if a["status"] in ["APPLIED", "REVIEWING"]]), "subtitle": "Pending evaluation", "icon": "search", "color": THEME["warning"]},
        {"title": "Offers Made", "value": len([a for a in apps if a["status"] == "OFFERED"]), "subtitle": "Final stage offers", "icon": "award", "color": THEME["success"]},
    ])

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Candidate Pipeline", "Open Requisitions", "Post New Job"])

    with tab1:
        st.subheader("Applicant Screening Pipeline")
        if apps:
            df_apps = pd.DataFrame(apps)
            cols = ["id", "job_title", "candidate_name", "candidate_email", "match_score", "status", "applied_at"]
            avail = [c for c in cols if c in df_apps.columns]

            st.dataframe(df_apps[avail], use_container_width=True, hide_index=True)

            st.markdown("#### Advance Candidate Status")
            col_sel, col_stat, col_btn = st.columns([2, 1, 1])
            with col_sel:
                app_id = st.selectbox("Select Candidate Application", options=[a["id"] for a in apps], format_func=lambda aid: f"App #{aid}: {[a['candidate_name'] for a in apps if a['id'] == aid][0]} - {[a['job_title'] for a in apps if a['id'] == aid][0]}")
            with col_stat:
                new_status = st.selectbox("Stage", ["REVIEWING", "INTERVIEW_SCHEDULED", "OFFERED", "REJECTED", "HIRED"])
            with col_btn:
                st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
                if st.button("Update Stage", use_container_width=True):
                    RecruitmentService.update_application_status(app_id, new_status)
                    st.success("Candidate stage updated successfully!")
                    st.rerun()
        else:
            empty_state("No Applications Received", "Job applications will appear here when candidates apply.")

    with tab2:
        st.subheader("Job Requisitions")
        if jobs:
            for j in jobs:
                st.markdown(f"""
                <div class="ts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: {THEME['dark_blue']};">{j['title']}</h4>
                        <span class="ts-badge ts-badge-blue">{j['status']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: {THEME['secondary']}; margin: 0.35rem 0;">
                        {j['department']} • {j['location']} • {j['job_type']} • {j['experience_level']}
                    </div>
                    <p style="font-size: 0.9rem; margin: 0.5rem 0;">{j['description']}</p>
                    <div style="font-size: 0.8rem; color: {THEME['primary']};">
                        <strong>Required Skills:</strong> {', '.join(j.get('required_skills', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("No Job Requisitions", "Post a requisition to start hiring.")

    with tab3:
        st.subheader("Create New Job Requisition")

        with st.expander("✨ AI Job Requisition Copilot (Auto-Generate Requirements & Salary Benchmark)", expanded=True):
            col_ai1, col_ai2, col_ai3 = st.columns([2, 1, 1])
            with col_ai1:
                ai_role_track = st.selectbox(
                    "Target Role Family",
                    ["Software / Backend Engineering", "AI / Machine Learning", "Cloud DevOps & SRE", "Talent Acquisition / HR"],
                    key="ai_role_track_select"
                )
            with col_ai2:
                ai_seniority = st.selectbox(
                    "Seniority Level",
                    ["Junior / Associate", "Senior", "Lead / Principal"],
                    index=1,
                    key="ai_seniority_select"
                )
            with col_ai3:
                st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
                if st.button("⚡ Generate with AI", use_container_width=True):
                    gen_spec = JobRequisitionGenerator.generate_job_spec(ai_role_track, seniority=ai_seniority)
                    st.session_state["gen_job_spec"] = gen_spec
                    st.success("Requisition generated! Review and publish below.")

        gen_spec = st.session_state.get("gen_job_spec", {})
        if gen_spec:
            stat_row([
                {"title": "Target Level", "value": gen_spec["seniority"], "subtitle": f"{gen_spec['experience_required']} Years Required", "icon": "briefcase", "color": THEME["primary"]},
                {"title": "Salary Benchmark", "value": f"${int(gen_spec['min_salary']):,} - ${int(gen_spec['max_salary']):,}", "subtitle": "Annual compensation band", "icon": "award", "color": THEME["success"]}
            ])
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        default_title = gen_spec.get("title", "")
        default_dept = "Engineering" if "Engineer" in default_title or "DevOps" in default_title or "ML" in default_title else "Human Resources"
        default_skills = gen_spec.get("required_skills", "Python, Docker, AWS, Kubernetes")
        default_desc = gen_spec.get("description", "Lead enterprise cloud modernization projects, architect microservices...")

        with st.form("create_job_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Job Title*", value=default_title, placeholder="e.g. Senior Backend Engineer")
                dept = st.text_input("Department*", value=default_dept, placeholder="e.g. Engineering")
                loc = st.selectbox("Location", ["Remote", "Hybrid - New York", "Hybrid - San Francisco", "On-Site"])
            with col2:
                job_type = st.selectbox("Job Type", ["Full-Time", "Contract", "Internship", "Part-Time"])
                exp_level = st.selectbox("Experience Level", ["Senior", "Mid-Level", "Entry-Level", "Lead / Staff"])
                skills_raw = st.text_input("Required Skills (comma separated)", value=default_skills)

            desc = st.text_area("Job Description", value=default_desc, height=120)
            reqs = st.text_area("Requirements & Qualifications", "5+ years of software development experience, BS/MS in Computer Science or equivalent practical experience.")

            submit_job = st.form_submit_button("Publish Job Requisition", use_container_width=True)
            if submit_job:
                if not title or not dept:
                    st.error("Please fill in Job Title and Department.")
                else:
                    skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
                    RecruitmentService.create_job(
                        title=title,
                        department=dept,
                        location=loc,
                        job_type=job_type,
                        experience_level=exp_level,
                        description=desc,
                        requirements=reqs,
                        required_skills=skills_list
                    )
                    st.success(f"Job requisition '{title}' published successfully!")
                    st.rerun()

def render_candidate_job_board(current_user: dict):
    page_header("Enterprise Job Opportunities", "Explore open roles across departments and submit your application with one click.", "Careers", "blue")

    jobs = RecruitmentService.get_all_jobs(status="OPEN")
    if not jobs:
        empty_state("No Openings Currently Available", "Check back soon for new opportunities.")
        return

    for j in jobs:
        with st.container():
            st.markdown(f"""
            <div class="ts-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: {THEME['dark_blue']};">{j['title']}</h4>
                    <span class="ts-badge ts-badge-green">HIRING</span>
                </div>
                <div style="font-size: 0.85rem; color: {THEME['secondary']}; margin: 0.25rem 0;">
                    {j['department']} • {j['location']} • {j['job_type']}
                </div>
                <p style="font-size: 0.9rem; margin: 0.5rem 0;">{j['description']}</p>
                <div style="font-size: 0.8rem; margin-bottom: 0.5rem;">
                    <strong>Skills:</strong> {', '.join(j.get('required_skills', []))}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Apply for {j['title']}", key=f"apply_btn_{j['id']}"):
                res = RecruitmentService.submit_application(job_id=j["id"], candidate_id=current_user["id"], match_score=85.0)
                if res.get("already_applied"):
                    st.info("You have already submitted an application for this role.")
                else:
                    st.success("Your application has been received! Recruiters will review your profile.")
