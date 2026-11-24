"""
TalentSphere Enterprise 2.0 - Recruitment Service
Handles Job Postings, Candidate Applications, Pipeline Tracking, and Interview Scheduling.
"""

from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.recruitment import JobDescription, CandidateApplication, JobMatch
from database.models.employee import Department
from core.exceptions import EntityNotFoundError, ValidationError
from core.logging import get_logger

logger = get_logger("recruitment_service")

class RecruitmentService:
    @staticmethod
    def get_all_jobs(status: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(JobDescription)
            if status:
                query = query.filter(JobDescription.status.ilike(status))
            jobs = query.order_by(JobDescription.created_at.desc()).all()

            results = []
            for j in jobs:
                dept_name = j.department.name if j.department else "Engineering"
                skills = [s.strip() for s in (j.required_skills or "").split(",") if s.strip()]
                results.append({
                    "id": j.id,
                    "title": j.title,
                    "department": dept_name,
                    "location": "Remote / HQ",
                    "job_type": j.employment_type or "Full-Time",
                    "experience_level": f"{j.experience_required}+ Yrs",
                    "description": j.description or "",
                    "requirements": j.description or "",
                    "required_skills": skills,
                    "status": j.status,
                    "applications_count": len(j.applications) if j.applications else 0,
                    "created_at": str(j.created_at.date()) if j.created_at else ""
                })
            return results

    @staticmethod
    def create_job(
        title: str,
        department: str,
        location: str,
        job_type: str,
        experience_level: str,
        description: str,
        requirements: str,
        required_skills: List[str]
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            dept = db.query(Department).filter(Department.name.ilike(department)).first()
            dept_id = dept.id if dept else None

            job = JobDescription(
                title=title,
                department_id=dept_id,
                employment_type=job_type,
                experience_required=3.0,
                required_skills=", ".join(required_skills),
                description=description,
                status="Open"
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            logger.info(f"Created job posting {job.id}: {job.title}")
            return {"id": job.id, "title": job.title}

    @staticmethod
    def get_applications(job_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(CandidateApplication)
            if job_id:
                query = query.filter(CandidateApplication.job_id == job_id)
            apps = query.order_by(CandidateApplication.created_at.desc()).all()

            results = []
            for a in apps:
                results.append({
                    "id": a.id,
                    "job_id": a.job_id,
                    "job_title": a.job.title if a.job else "Open Requisition",
                    "candidate_id": 1,
                    "candidate_name": a.candidate_name,
                    "candidate_email": a.candidate_email,
                    "match_score": 88.0,
                    "status": a.status,
                    "applied_at": str(a.created_at.date()) if a.created_at else ""
                })
            return results

    @staticmethod
    def submit_application(job_id: int, candidate_id: int, match_score: float = 0.0) -> Dict[str, Any]:
        with get_db_session() as db:
            from database.models.user import User
            user = db.query(User).filter(User.id == candidate_id).first()
            name = user.full_name or user.username if user else "Candidate"
            email = user.email if user else "candidate@example.com"

            app = CandidateApplication(
                job_id=job_id,
                candidate_name=name,
                candidate_email=email,
                status="Applied"
            )
            db.add(app)
            db.commit()
            db.refresh(app)
            return {"id": app.id, "status": app.status, "already_applied": False}

    @staticmethod
    def update_application_status(application_id: int, new_status: str) -> bool:
        with get_db_session() as db:
            app = db.query(CandidateApplication).filter(CandidateApplication.id == application_id).first()
            if not app:
                raise EntityNotFoundError("CandidateApplication", application_id)
            app.status = new_status
            db.commit()
            return True
