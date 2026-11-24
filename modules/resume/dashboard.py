"""
TalentSphere Enterprise 2.0 - Resume & ATS Analyzer Module
Interactive resume upload, skill extraction, and ATS scoring engine.
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, metric_card, stat_row, empty_state
from ai_engine.resume_analyzer import ResumeAnalyzer
from ai_engine.ats_engine import ATSEngine
from ai_engine.job_matcher import JobMatcher
from services.recruitment_service import RecruitmentService

def render_resume_module(current_user: dict):
    page_header("AI Resume & ATS Intelligence", "Analyze resume hygiene, extract competencies, and optimize for enterprise ATS algorithms.", "AI Engine", "blue")

    col_upload, col_target = st.columns([1, 1])

    with col_upload:
        st.subheader("1. Upload Candidate Resume")
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT Document", type=["pdf", "docx", "txt"], key="resume_uploader")
        resume_text = ""
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            resume_data = ResumeAnalyzer.parse_resume(file_bytes, uploaded_file.name)
            resume_text = resume_data["raw_text"]
            st.session_state["parsed_resume"] = resume_data
            st.success(f"Extracted {resume_data['word_count']} words from {uploaded_file.name}")
        elif "parsed_resume" in st.session_state:
            resume_data = st.session_state["parsed_resume"]
            resume_text = resume_data["raw_text"]
        else:
            resume_text = """
            Senior Software Engineer with 5+ years of experience building scalable distributed web applications.
            Skilled in Python, FastAPI, Django, React, TypeScript, Docker, Kubernetes, AWS, PostgreSQL, Redis, and Git.
            Experience: Led backend architecture for payment processing service handling 2M requests/day.
            Education: B.S. in Computer Science.
            Projects: Built microservices using CI/CD pipelines and Docker containers.
            Certifications: AWS Certified Solutions Architect.
            """
            st.info("No file uploaded yet. Using demo resume text for preview:")

    with col_target:
        st.subheader("2. Target Job Description")
        jobs = RecruitmentService.get_all_jobs()
        job_options = {j["id"]: j["title"] for j in jobs}
        
        target_jd = ""
        target_skills = []

        if jobs:
            selected_job_id = st.selectbox("Select Existing Job Requisition", options=list(job_options.keys()), format_func=lambda x: job_options[x])
            job_obj = next((j for j in jobs if j["id"] == selected_job_id), None)
            if job_obj:
                target_jd = f"{job_obj['title']} {job_obj['description']} {job_obj['requirements']}"
                target_skills = job_obj.get("required_skills", [])
        else:
            target_jd = st.text_area("Paste Target Job Description", "Seeking Senior Python Engineer with expertise in FastAPI, Docker, Kubernetes, SQL, AWS, and Agile practices.")
            target_skills = ["Python", "FastAPI", "Docker", "AWS", "Kubernetes", "SQL"]

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    if st.button("Run ATS Score & Competency Diagnostic", type="primary", use_container_width=True):
        st.session_state["ats_result"] = ATSEngine.compute_ats_score(resume_text, target_jd, target_skills)

    if "ats_result" in st.session_state:
        res = st.session_state["ats_result"]

        st.subheader("ATS Diagnostic Results")
        stat_row([
            {"title": "Overall ATS Score", "value": f"{res['overall_score']}%", "subtitle": "Composite match rating", "icon": "award", "color": THEME["primary"] if res["overall_score"] >= 70 else THEME["warning"]},
            {"title": "Semantic Relevance", "value": f"{res['semantic_score']}%", "subtitle": "TF-IDF similarity", "icon": "cpu", "color": THEME["dark_blue"]},
            {"title": "Keyword Coverage", "value": f"{res['keyword_score']}%", "subtitle": "Target skill presence", "icon": "search", "color": THEME["success"]},
            {"title": "Structure Hygiene", "value": f"{res['structure_score']}%", "subtitle": "Standard sections present", "icon": "file_text", "color": THEME["warning"]},
        ])

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            matched_items = ', '.join(res['matched_keywords']) if res['matched_keywords'] else 'None identified'
            st.markdown(f"""
            <div class="ts-card" style="border-top: 4px solid #16A34A !important;">
                <h4 style="margin: 0 0 0.5rem 0; color: #15803D !important; font-weight: 700;">Matched Keywords ({len(res['matched_keywords'])})</h4>
                <div style="color: #0F172A !important; font-size: 0.95rem; font-weight: 500; line-height: 1.6;">{matched_items}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_k2:
            missing_items = ', '.join(res['missing_keywords']) if res['missing_keywords'] else 'All key skills covered!'
            st.markdown(f"""
            <div class="ts-card" style="border-top: 4px solid #DC2626 !important;">
                <h4 style="margin: 0 0 0.5rem 0; color: #B91C1C !important; font-weight: 700;">Missing Keywords ({len(res['missing_keywords'])})</h4>
                <div style="color: #0F172A !important; font-size: 0.95rem; font-weight: 500; line-height: 1.6;">{missing_items}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Actionable AI Recommendations")
        for rec in res["recommendations"]:
            st.info(f"💡 {rec}")
