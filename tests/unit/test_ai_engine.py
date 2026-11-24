"""
Unit tests for AI Engine, ATS Scoring, Job Matching, and Career Recommender
"""

import pytest
from ai_engine.resume_analyzer import ResumeAnalyzer
from ai_engine.ats_engine import ATSEngine
from ai_engine.job_matcher import JobMatcher
from ai_engine.career_recommender import CareerRecommender
from ai_engine.skill_analyzer import SkillAnalyzer

SAMPLE_RESUME = """
Jane Doe
Email: jane.doe@enterprise.com
Phone: (555) 234-5678

Summary:
Experienced Software Engineer proficient in Python, FastAPI, Docker, SQL, Git, and Kubernetes.
Experience:
Senior Developer at CloudTech. Built microservices architectures.
Education:
B.S. in Computer Science.
Projects:
Developed distributed API system handling 50k requests per minute.
Certifications:
AWS Certified Developer.
"""

def test_resume_analyzer_text_and_skills():
    contacts = ResumeAnalyzer.extract_contact_info(SAMPLE_RESUME)
    assert contacts["email"] == "jane.doe@enterprise.com"
    assert "555" in contacts["phone"]

    skills = ResumeAnalyzer.extract_skills(SAMPLE_RESUME)
    skills_lower = [s.lower() for s in skills]
    assert "python" in skills_lower
    assert "docker" in skills_lower
    assert "fastapi" in skills_lower
    assert "sql" in skills_lower

def test_ats_engine_scoring():
    job_desc = "Seeking a Python engineer with Docker, FastAPI, Kubernetes, and Git experience."
    result = ATSEngine.compute_ats_score(SAMPLE_RESUME, job_desc, ["Python", "Docker", "FastAPI", "Kubernetes"])
    
    assert result["overall_score"] >= 50.0
    assert result["keyword_score"] >= 75.0
    assert len(result["matched_keywords"]) > 0
    assert isinstance(result["recommendations"], list)

def test_job_matcher_cosine_similarity():
    jobs = [
        {"id": 1, "title": "Python Cloud Engineer", "department": "Engineering", "description": "Python, Docker, AWS, FastAPI", "requirements": "Python, Git"},
        {"id": 2, "title": "Registered Nurse", "department": "Healthcare", "description": "Patient triage and medication delivery", "requirements": "RN License"}
    ]
    ranked = JobMatcher.match_resume_to_jobs(SAMPLE_RESUME, jobs)
    assert len(ranked) == 2
    assert ranked[0]["id"] == 1  # Software engineer role must rank first
    assert ranked[0]["match_score"] > ranked[1]["match_score"]

def test_skill_gap_analyzer():
    user_skills = ["Python", "FastAPI", "SQL"]
    target_role_skills = ["Python", "FastAPI", "SQL", "Docker", "Kubernetes"]

    gap = SkillAnalyzer.analyze_skill_gap(user_skills, target_role_skills)
    assert gap["readiness_percentage"] == 60.0
    assert gap["gap_count"] == 2
    assert "Docker" in gap["missing_skills"]
    assert "Kubernetes" in gap["missing_skills"]

def test_career_recommender():
    user_skills = ["Python", "Docker", "AWS", "Kubernetes", "Linux"]
    recs = CareerRecommender.recommend_roles(user_skills)
    assert len(recs) > 0
    assert recs[0]["role"] == "Cloud DevOps Engineer"
    assert recs[0]["match_percentage"] >= 50.0
