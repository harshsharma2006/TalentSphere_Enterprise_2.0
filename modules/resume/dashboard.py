"""
TalentSphere Enterprise 2.0 - Resume & ATS Analyzer Module
Interactive resume upload, skill extraction, ATS scoring engine, and AI bullet optimizer.
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, metric_card, stat_row, empty_state
from ai_engine.resume_analyzer import ResumeAnalyzer
from ai_engine.ats_engine import ATSEngine
from ai_engine.job_matcher import JobMatcher
from ai_engine.resume_optimizer import ResumeBulletOptimizer
from services.recruitment_service import RecruitmentService

def render_resume_module(current_user: dict):
    page_header("AI Resume & ATS Intelligence", "Analyze resume hygiene, extract competencies, and optimize for enterprise ATS algorithms.", "AI Engine", "blue")

    tab_ats, tab_opt = st.tabs(["📊 ATS Score & Competency Diagnostic", "✨ AI Resume Bullet Optimizer & Rewriter"])

    with tab_ats:
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

    with tab_opt:
        st.subheader("✨ AI Resume Bullet Point Optimizer (STAR Method)")
        st.write("Convert plain task statements into high-impact, quantifiable achievements calibrated for enterprise ATS algorithms and engineering hiring managers.")

        bullet_input = st.text_area(
            "Paste a Raw Candidate Resume Bullet Point",
            "Worked with python and docker to build APIs and fix backend performance issues",
            help="Enter any generic responsibility or project bullet point to rewrite using the STAR methodology."
        )

        col_dom, col_btn = st.columns([2, 1])
        with col_dom:
            domain_sel = st.selectbox(
                "Target Engineering Discipline",
                ["Backend / Cloud Engineering", "Machine Learning & AI", "DevOps & Infrastructure", "Full-Stack Development"]
            )
        with col_btn:
            st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
            opt_clicked = st.button("✨ Optimize Bullet with AI", type="primary", use_container_width=True)

        if opt_clicked or "last_optimized_bullet" in st.session_state:
            if opt_clicked:
                st.session_state["last_optimized_bullet"] = bullet_input
                st.session_state["bullet_analysis"] = ResumeBulletOptimizer.analyze_bullet(bullet_input)
                st.session_state["bullet_variants"] = ResumeBulletOptimizer.optimize_bullet(bullet_input, domain_sel)

            analysis = st.session_state.get("bullet_analysis", {})
            variants = st.session_state.get("bullet_variants", [])

            if analysis:
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                score_color = THEME["success"] if analysis["impact_score"] >= 75 else THEME["warning"]
                stat_row([
                    {"title": "Initial Impact Rating", "value": f"{int(analysis['impact_score'])}/100", "subtitle": "Candidate baseline", "icon": "award", "color": score_color},
                    {"title": "Active Power Verb", "value": "Detected" if analysis['has_action_verb'] else "Missing", "subtitle": f"Lead: '{analysis['lead_verb']}'", "icon": "cpu", "color": THEME["primary"] if analysis['has_action_verb'] else THEME["danger"]},
                    {"title": "Quantified Metrics", "value": "Present" if analysis['has_metrics'] else "None Found", "subtitle": "Numbers, % or throughput", "icon": "bar_chart", "color": THEME["success"] if analysis['has_metrics'] else THEME["warning"]},
                    {"title": "Tech Keywords", "value": str(len(analysis['detected_keywords'])), "subtitle": ", ".join(analysis['detected_keywords'][:3]) if analysis['detected_keywords'] else "None detected", "icon": "search", "color": THEME["dark_blue"]}
                ])

                st.markdown("#### 🎯 AI-Generated STAR Optimized Bullet Variants")
                for idx, var in enumerate(variants):
                    st.markdown(f"""
                    <div class="ts-card" style="border-left: 4px solid {THEME['primary']}; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-weight: 700; color: {THEME['dark_blue']}; font-size: 1rem;">Variant #{idx+1}: {var['style']}</span>
                            <span class="ts-badge ts-badge-blue">{var['action_verb']}</span>
                        </div>
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 0.75rem 1rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 0.95rem; color: #0F172A; line-height: 1.6; margin: 0.5rem 0;">
                            <strong>•</strong> {var['text']}
                        </div>
                        <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: #64748B; margin-top: 0.35rem;">
                            <span><strong>Metric Focus:</strong> {var['metric']}</span>
                            <span>•</span>
                            <span><strong>Framework:</strong> {var['framework']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
