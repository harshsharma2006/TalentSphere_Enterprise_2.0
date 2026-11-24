"""
Resume and ATS Analysis Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Resume(Base, IDMixin, TimestampMixin):
    """Uploaded Resume Document."""
    __tablename__ = "resumes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(150), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    file_type = Column(String(20), default="pdf")
    extracted_text = Column(Text, nullable=True)

    analyses = relationship("ResumeAnalysis", back_populates="resume", cascade="all, delete-orphan")

class ResumeAnalysis(Base, IDMixin, TimestampMixin):
    """Detailed ATS Scoring & Intelligence Record."""
    __tablename__ = "resume_analyses"

    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    ats_score = Column(Float, nullable=False) # 0 to 100
    contact_info_json = Column(Text, nullable=True)
    extracted_skills_json = Column(Text, nullable=True)
    education_json = Column(Text, nullable=True)
    experience_json = Column(Text, nullable=True)
    strengths_json = Column(Text, nullable=True)
    improvements_json = Column(Text, nullable=True)
    missing_keywords_json = Column(Text, nullable=True)
    target_job_title = Column(String(150), nullable=True)

    resume = relationship("Resume", back_populates="analyses")
