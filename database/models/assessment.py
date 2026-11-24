"""
Assessment and Assessment Result Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Assessment(Base, IDMixin, TimestampMixin):
    """Psychometric, Coding, or Aptitude Assessment."""
    __tablename__ = "assessments"

    title = Column(String(150), nullable=False, index=True)
    assessment_type = Column(String(50), default="Aptitude") # Aptitude, Coding, Soft Skills, Interest
    duration_minutes = Column(Integer, default=30)
    questions_json = Column(Text, nullable=False) # JSON list of questions, choices, answers

    results = relationship("AssessmentResult", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentResult(Base, IDMixin, TimestampMixin):
    """User Score and Performance on an Assessment."""
    __tablename__ = "assessment_results"

    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score_pct = Column(Float, nullable=False)
    total_questions = Column(Integer, default=10)
    correct_answers = Column(Integer, default=0)
    answers_json = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)

    assessment = relationship("Assessment", back_populates="results")
    user = relationship("User", back_populates="assessment_results")
