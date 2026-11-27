"""
Unit tests for newly added AI engine features in TalentSphere Enterprise 2.0.
Tests ResumeBulletOptimizer, InterviewSimulator, JobRequisitionGenerator, and AICareerMentor.
"""

import pytest
from ai_engine.resume_optimizer import ResumeBulletOptimizer
from ai_engine.interview_simulator import InterviewSimulator
from ai_engine.job_generator import JobRequisitionGenerator
from ai_engine.ai_mentor import AICareerMentor

def test_resume_bullet_optimizer_analysis():
    raw_bullet = "Engineered automated CI/CD pipeline using Docker and Kubernetes, reducing build times by 40%."
    analysis = ResumeBulletOptimizer.analyze_bullet(raw_bullet)
    assert analysis["has_action_verb"] is True
    assert analysis["has_metrics"] is True
    assert "Docker" in analysis["detected_keywords"] or "Kubernetes" in analysis["detected_keywords"]
    assert analysis["impact_score"] >= 80.0

def test_resume_bullet_optimizer_variants():
    raw_bullet = "Worked with Python and PostgreSQL to fix database performance."
    variants = ResumeBulletOptimizer.optimize_bullet(raw_bullet, "Backend / Cloud Engineering")
    assert len(variants) == 3
    for v in variants:
        assert "text" in v
        assert "action_verb" in v
        assert "metric" in v
        assert "framework" in v

def test_interview_simulator_roles_and_questions():
    roles = InterviewSimulator.get_roles()
    assert len(roles) >= 3
    assert "Senior Backend Engineer" in roles

    questions = InterviewSimulator.get_questions_for_role("Senior Backend Engineer")
    assert len(questions) >= 1
    q = questions[0]
    assert "question" in q
    assert "expected_concepts" in q
    assert "model_answer" in q

def test_interview_simulator_evaluation():
    questions = InterviewSimulator.get_questions_for_role("Senior Backend Engineer")
    q = questions[0]
    user_answer = (
        "In our system, we deployed a Redis cluster to cache high-frequency requests with TTL invalidation. "
        "To prevent cache stampedes, we implemented write-through caching with background workers, reducing database latency."
    )
    result = InterviewSimulator.evaluate_response(q, user_answer)
    assert result["overall_score"] > 50.0
    assert len(result["matched_concepts"]) > 0
    assert len(result["feedback"]) > 0
    assert result["star_score"] > 0

def test_job_requisition_generator():
    spec = JobRequisitionGenerator.generate_job_spec("software", seniority="Senior")
    assert "title" in spec
    assert "required_skills" in spec
    assert spec["min_salary"] > 0
    assert spec["max_salary"] > spec["min_salary"]
    assert "description" in spec

    ml_spec = JobRequisitionGenerator.generate_job_spec("ai_ml", seniority="Lead / Principal")
    assert "Machine Learning" in ml_spec["title"] or "AI" in ml_spec["title"]
    assert ml_spec["min_salary"] > spec["min_salary"]

def test_ai_career_mentor():
    advice_devops = AICareerMentor.get_advice("How do I transition to cloud and devops?")
    assert advice_devops["is_matched"] is True
    assert "DevOps" in advice_devops["category"] or "Cloud" in advice_devops["category"]
    assert len(advice_devops["guidance"]) > 50

    fallback = AICareerMentor.get_advice("Random non-matching engineering topic")
    assert "guidance" in fallback
