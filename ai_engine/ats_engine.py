"""
TalentSphere Enterprise 2.0 - ATS Engine
Applicant Tracking System Scoring and Keyword Gap Optimizer.
"""

import re
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_engine.resume_analyzer import ResumeAnalyzer

STANDARD_SECTIONS = ["experience", "education", "skills", "projects", "certifications"]

class ATSEngine:
    @staticmethod
    def compute_ats_score(resume_text: str, job_description: str, target_skills: List[str] = None) -> Dict[str, Any]:
        """
        Computes a comprehensive ATS score (0-100) based on:
        1. Semantic Cosine Similarity (TF-IDF) (35%)
        2. Target Skills & Keyword Coverage (35%)
        3. Structural Section Presence (15%)
        4. Readability & Formatting Hygiene (15%)
        """
        if not resume_text.strip():
            return {
                "overall_score": 0.0,
                "semantic_score": 0.0,
                "keyword_score": 0.0,
                "structure_score": 0.0,
                "readability_score": 0.0,
                "matched_keywords": [],
                "missing_keywords": [],
                "recommendations": ["Resume text is empty. Upload a valid document."]
            }

        # 1. Semantic Similarity
        try:
            tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = tfidf.fit_transform([resume_text, job_description])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            semantic_score = round(float(sim) * 100, 1)
        except Exception:
            semantic_score = 45.0

        # 2. Keyword Coverage
        extracted_skills = [s.lower() for s in ResumeAnalyzer.extract_skills(resume_text)]
        if not target_skills:
            target_skills = [s.lower() for s in ResumeAnalyzer.extract_skills(job_description)]
            if not target_skills:
                target_skills = ["python", "sql", "git", "communication"]

        target_skills_clean = [s.lower().strip() for s in target_skills]
        matched_kw = [s for s in target_skills_clean if s in extracted_skills or re.search(r'\b' + re.escape(s) + r'\b', resume_text.lower())]
        missing_kw = [s for s in target_skills_clean if s not in matched_kw]

        keyword_score = round((len(matched_kw) / max(len(target_skills_clean), 1)) * 100, 1)

        # 3. Structure Score
        present_sections = []
        lower_resume = resume_text.lower()
        for sec in STANDARD_SECTIONS:
            if re.search(r'\b' + sec + r'\b', lower_resume):
                present_sections.append(sec)
        structure_score = round((len(present_sections) / len(STANDARD_SECTIONS)) * 100, 1)

        # 4. Readability Score
        words = resume_text.split()
        word_count = len(words)
        if 250 <= word_count <= 1000:
            readability_score = 95.0
        elif 150 <= word_count < 250 or 1000 < word_count <= 1500:
            readability_score = 75.0
        else:
            readability_score = 50.0

        # Weighted Composite Score
        overall = (
            (semantic_score * 0.35) +
            (keyword_score * 0.35) +
            (structure_score * 0.15) +
            (readability_score * 0.15)
        )
        overall_score = round(min(100.0, max(0.0, overall)), 1)

        # Recommendations
        recommendations = []
        if missing_kw:
            recommendations.append(f"Incorporate missing core skills: {', '.join(missing_kw[:5])}.")
        if len(present_sections) < len(STANDARD_SECTIONS):
            missing_sec = [s.title() for s in STANDARD_SECTIONS if s not in present_sections]
            recommendations.append(f"Add missing standard sections: {', '.join(missing_sec)}.")
        if word_count < 250:
            recommendations.append("Resume is brief. Expand on technical project contributions and business impact.")
        elif word_count > 1000:
            recommendations.append("Resume exceeds recommended 2-page length. Condense bullet points.")
        if overall_score >= 80:
            recommendations.append("Strong ATS alignment! Formatting and keywords meet enterprise standards.")

        return {
            "overall_score": overall_score,
            "semantic_score": semantic_score,
            "keyword_score": keyword_score,
            "structure_score": structure_score,
            "readability_score": readability_score,
            "matched_keywords": [s.title() for s in matched_kw],
            "missing_keywords": [s.title() for s in missing_kw],
            "recommendations": recommendations
        }
