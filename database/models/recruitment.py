"""
Job Description, Candidate Application, Interview, and Job Matching Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class JobDescription(Base, IDMixin, TimestampMixin):
    """Requisition / Job Opening."""
    __tablename__ = "job_descriptions"

    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(150), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    employment_type = Column(String(50), default="Full-Time")
    experience_required = Column(Float, default=0.0)
    min_salary = Column(Float, nullable=True)
    max_salary = Column(Float, nullable=True)
    required_skills = Column(Text, nullable=False) # comma-separated or json
    description = Column(Text, nullable=False)
    status = Column(String(30), default="Open") # Open, Closed, Draft

    department = relationship("Department", back_populates="job_descriptions")
    applications = relationship("CandidateApplication", back_populates="job", cascade="all, delete-orphan")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")

class CandidateApplication(Base, IDMixin, TimestampMixin):
    """Candidate Applicant Profile."""
    __tablename__ = "candidate_applications"

    job_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="SET NULL"), nullable=True, index=True)
    candidate_name = Column(String(120), nullable=False)
    candidate_email = Column(String(120), nullable=False, index=True)
    candidate_phone = Column(String(30), nullable=True)
    current_role = Column(String(100), nullable=True)
    total_experience_years = Column(Float, default=0.0)
    skills = Column(Text, nullable=True)
    resume_path = Column(String(255), nullable=True)
    resume_filename = Column(String(150), nullable=True)
    extracted_text = Column(Text, nullable=True)
    status = Column(String(30), default="Applied") # Applied, Shortlisted, Interview, Selected, Rejected
    notes = Column(Text, nullable=True)

    job = relationship("JobDescription", back_populates="applications")
    interviews = relationship("CandidateInterview", back_populates="application", cascade="all, delete-orphan")
    matches = relationship("JobMatch", back_populates="application", cascade="all, delete-orphan")

class CandidateInterview(Base, IDMixin, TimestampMixin):
    """Candidate Interview Schedule & Evaluation."""
    __tablename__ = "candidate_interviews"

    application_id = Column(Integer, ForeignKey("candidate_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    interviewer_name = Column(String(100), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    interview_mode = Column(String(40), default="Online Video") # Online Video, In-Person, Phone
    meeting_link = Column(String(255), nullable=True)
    status = Column(String(30), default="Scheduled") # Scheduled, Completed, Cancelled
    rating = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)

    application = relationship("CandidateApplication", back_populates="interviews")

class JobMatch(Base, IDMixin, TimestampMixin):
    """AI Matching Record linking Candidate to Job Specification."""
    __tablename__ = "job_matches"

    job_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id = Column(Integer, ForeignKey("candidate_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    match_score = Column(Float, nullable=False) # 0.0 to 100.0
    matched_skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)

    job = relationship("JobDescription", back_populates="matches")
    application = relationship("CandidateApplication", back_populates="matches")
