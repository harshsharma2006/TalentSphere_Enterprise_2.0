"""
TalentSphere Enterprise 2.0 - Performance Service
Handles Performance Reviews, KPI Goals, Ratings, and Continuous Feedback.
"""

from datetime import date
from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.performance import PerformanceReview, EmployeeGoal, KPI
from database.models.employee import Employee
from core.exceptions import EntityNotFoundError
from core.logging import get_logger

logger = get_logger("performance_service")

class PerformanceService:
    @staticmethod
    def get_all_reviews(employee_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(PerformanceReview)
            if employee_id:
                query = query.filter(PerformanceReview.employee_id == employee_id)
            reviews = query.order_by(PerformanceReview.created_at.desc()).all()

            results = []
            for r in reviews:
                emp_name = r.employee.full_name if r.employee else "Employee"
                results.append({
                    "id": r.id,
                    "employee_id": r.employee_id,
                    "employee_name": emp_name,
                    "reviewer_id": r.reviewer_id,
                    "reviewer_name": r.reviewer_name or "HR Manager",
                    "review_cycle": r.review_period,
                    "overall_score": float(r.overall_rating or 0.0),
                    "status": "COMPLETED",
                    "manager_feedback": r.achievements or "",
                    "strengths": r.achievements or "",
                    "areas_for_improvement": r.growth_areas or "",
                    "created_at": str(r.created_at.date()) if r.created_at else ""
                })
            return results

    @staticmethod
    def create_review(
        employee_id: int,
        reviewer_id: Optional[int],
        review_cycle: str,
        overall_score: float,
        manager_feedback: str,
        strengths: str = "",
        areas_for_improvement: str = ""
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            review = PerformanceReview(
                employee_id=employee_id,
                reviewer_id=reviewer_id,
                review_period=review_cycle,
                overall_rating=overall_score,
                technical_rating=overall_score,
                leadership_rating=overall_score,
                communication_rating=overall_score,
                achievements=f"{strengths}. {manager_feedback}",
                growth_areas=areas_for_improvement or "Continuous skill progression",
                reviewer_name="Engineering Manager"
            )
            db.add(review)
            db.commit()
            db.refresh(review)
            logger.info(f"Created performance review {review.id} for employee {employee_id}")
            return {"id": review.id, "review_cycle": review.review_period, "score": review.overall_rating}

    @staticmethod
    def get_employee_goals(employee_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            goals = db.query(EmployeeGoal).filter(EmployeeGoal.employee_id == employee_id).all()
            return [
                {
                    "id": g.id,
                    "title": g.title,
                    "description": g.description,
                    "progress_percentage": g.progress_pct,
                    "target_date": str(g.due_date) if g.due_date else "",
                    "status": g.status,
                    "weightage": 1.0
                }
                for g in goals
            ]

    @staticmethod
    def create_goal(employee_id: int, title: str, description: str, target_date: date, weightage: float = 1.0) -> Dict[str, Any]:
        with get_db_session() as db:
            goal = EmployeeGoal(
                employee_id=employee_id,
                title=title,
                description=description,
                due_date=target_date,
                progress_pct=0,
                status="In Progress"
            )
            db.add(goal)
            db.commit()
            db.refresh(goal)
            return {"id": goal.id, "title": goal.title}

    @staticmethod
    def update_goal_progress(goal_id: int, progress: int) -> bool:
        with get_db_session() as db:
            g = db.query(EmployeeGoal).filter(EmployeeGoal.id == goal_id).first()
            if not g:
                raise EntityNotFoundError("EmployeeGoal", goal_id)
            g.progress_pct = max(0, min(100, progress))
            if g.progress_pct == 100:
                g.status = "Achieved"
            db.commit()
            return True
