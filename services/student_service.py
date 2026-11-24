"""
TalentSphere Enterprise 2.0 - Student Service
Handles College Students, High School Students, Academic Profiles, and Placement Readiness.
"""

from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.student import Student
from database.models.user import User
from core.exceptions import EntityNotFoundError, ValidationError
from core.logging import get_logger

logger = get_logger("student_service")

class StudentService:
    @staticmethod
    def get_academic_departments() -> List[Dict[str, Any]]:
        """Returns standard academic departments."""
        return [
            {"id": 1, "name": "Computer Science & Engineering", "code": "CSE", "student_count": 120},
            {"id": 2, "name": "Information Technology", "code": "IT", "student_count": 85},
            {"id": 3, "name": "Data Science & AI", "code": "DSAI", "student_count": 60},
            {"id": 4, "name": "Pre-College STEM Division", "code": "STEM", "student_count": 45}
        ]

    @staticmethod
    def get_all_students(student_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Student)
            if student_type:
                query = query.filter(Student.student_type.ilike(f"%{student_type}%"))
            students = query.all()

            results = []
            for s in students:
                results.append({
                    "id": s.id,
                    "user_id": s.user_id,
                    "student_id_number": s.student_code,
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "full_name": s.full_name,
                    "email": s.email,
                    "student_type": s.student_type,
                    "department": s.major or "Computer Science",
                    "degree_program": s.degree_program or "B.S. CS",
                    "current_year": s.current_year or 1,
                    "gpa": float(s.cgpa_percentage or 0.0),
                    "placement_readiness_score": float(s.cgpa_percentage or 75.0),
                    "placement_status": s.placement_status or "Seeking"
                })
            return results

    @staticmethod
    def get_student_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            s = db.query(Student).filter(Student.user_id == user_id).first()
            if not s:
                return None
            return {
                "id": s.id,
                "user_id": s.user_id,
                "student_id_number": s.student_code,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "full_name": s.full_name,
                "email": s.email,
                "student_type": s.student_type,
                "department": s.major or "Computer Science",
                "degree_program": s.degree_program or "B.S. CS",
                "current_year": s.current_year or 1,
                "gpa": float(s.cgpa_percentage or 0.0),
                "placement_readiness_score": float(s.cgpa_percentage or 75.0),
                "placement_status": s.placement_status or "Seeking"
            }

    @staticmethod
    def update_placement_score(student_id: int, new_score: float) -> bool:
        with get_db_session() as db:
            s = db.query(Student).filter(Student.id == student_id).first()
            if not s:
                raise EntityNotFoundError("Student", student_id)
            s.cgpa_percentage = round(max(0.0, min(100.0, new_score)), 1)
            db.commit()
            return True
