"""
TalentSphere Enterprise 2.0 - Career Service
Handles Career Pathways, Succession Planning, Competency Milestones, and Promotion Readiness.
"""

from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.career import CareerGoal, CareerRoadmap
from core.exceptions import EntityNotFoundError
from core.logging import get_logger

logger = get_logger("career_service")

class CareerService:
    @staticmethod
    def get_all_career_paths() -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "department": "Engineering",
                "current_role": "Software Engineer",
                "target_role": "Senior Cloud DevOps Engineer",
                "typical_timeline_months": 12,
                "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "CI/CD"],
                "description": "Transition into infrastructure leadership and containerization."
            },
            {
                "id": 2,
                "department": "Data Science",
                "current_role": "Junior Data Analyst",
                "target_role": "Machine Learning Engineer",
                "typical_timeline_months": 18,
                "required_skills": ["Python", "PyTorch", "Scikit-Learn", "SQL", "MLOps"],
                "description": "Advance into predictive modeling and deep learning engineering."
            }
        ]

    @staticmethod
    def get_career_goals(user_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            goals = db.query(CareerGoal).filter(CareerGoal.user_id == user_id).all()
            return [
                {
                    "id": g.id,
                    "title": f"Path to {g.target_role}",
                    "target_role": g.target_role,
                    "target_timeline_months": 12,
                    "progress_percentage": int(g.readiness_score or 0),
                    "action_items": ["Complete cloud coursework", "Contribute to enterprise RFCs"],
                    "status": "Active"
                }
                for g in goals
            ]

    @staticmethod
    def create_career_goal(user_id: int, title: str, target_role: str, target_timeline_months: int, action_items: List[str]) -> Dict[str, Any]:
        with get_db_session() as db:
            cg = CareerGoal(
                user_id=user_id,
                target_role=target_role,
                timeline=f"{target_timeline_months} Months",
                career_statement=title,
                readiness_score=0.0
            )
            db.add(cg)
            db.commit()
            db.refresh(cg)
            return {"id": cg.id, "title": title}
