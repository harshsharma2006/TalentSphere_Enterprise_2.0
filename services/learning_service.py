"""
TalentSphere Enterprise 2.0 - Learning Service
Handles Course Catalog, Skill Upskilling Programs, Enrollments, and Certifications.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.learning import Course, CourseEnrollment, Certification
from core.exceptions import EntityNotFoundError
from core.logging import get_logger

logger = get_logger("learning_service")

class LearningService:
    @staticmethod
    def get_all_courses(category: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Course)
            if category:
                query = query.filter(Course.category.ilike(category))
            courses = query.all()
            return [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "category": c.category,
                    "provider": "TalentSphere Academy",
                    "duration_hours": c.duration_hours,
                    "skill_tags": [s.strip() for s in (c.target_skills or "").split(",") if s.strip()],
                    "level": c.difficulty_level,
                    "enrollment_count": len(c.enrollments) if c.enrollments else 0
                }
                for c in courses
            ]

    @staticmethod
    def get_user_enrollments(user_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            enrollments = db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user_id).all()
            results = []
            for e in enrollments:
                results.append({
                    "id": e.id,
                    "course_id": e.course_id,
                    "course_title": e.course.title if e.course else "Course",
                    "category": e.course.category if e.course else "Technical",
                    "duration_hours": e.course.duration_hours if e.course else 10,
                    "progress_percentage": e.progress_pct,
                    "status": e.status,
                    "enrolled_at": str(e.enrolled_at.date()) if e.enrolled_at else ""
                })
            return results

    @staticmethod
    def enroll_user(user_id: int, course_id: int) -> Dict[str, Any]:
        with get_db_session() as db:
            existing = db.query(CourseEnrollment).filter(
                CourseEnrollment.user_id == user_id,
                CourseEnrollment.course_id == course_id
            ).first()
            if existing:
                return {"id": existing.id, "already_enrolled": True, "progress": existing.progress_pct}

            enrollment = CourseEnrollment(
                user_id=user_id,
                course_id=course_id,
                progress_pct=0,
                status="In Progress",
                enrolled_at=datetime.utcnow()
            )
            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)
            return {"id": enrollment.id, "already_enrolled": False, "progress": 0}

    @staticmethod
    def update_progress(enrollment_id: int, progress: int) -> bool:
        with get_db_session() as db:
            e = db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()
            if not e:
                raise EntityNotFoundError("CourseEnrollment", enrollment_id)
            e.progress_pct = max(0, min(100, progress))
            if e.progress_pct == 100:
                e.status = "COMPLETED"
                e.completed_at = datetime.utcnow()
            db.commit()
            return True
