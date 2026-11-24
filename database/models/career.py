"""
Career Goals and AI Career Roadmaps Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class CareerGoal(Base, IDMixin, TimestampMixin):
    """User Target Career Destination."""
    __tablename__ = "career_goals"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = Column(String(100), nullable=False)
    timeline = Column(String(50), default="6-12 Months")
    career_statement = Column(Text, nullable=True)
    readiness_score = Column(Float, default=0.0)

    user = relationship("User", back_populates="career_goals")
    roadmaps = relationship("CareerRoadmap", back_populates="career_goal", cascade="all, delete-orphan")

class CareerRoadmap(Base, IDMixin, TimestampMixin):
    """Milestone-based development roadmap."""
    __tablename__ = "career_roadmaps"

    career_goal_id = Column(Integer, ForeignKey("career_goals.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    target_role = Column(String(100), nullable=False)
    steps_json = Column(Text, nullable=False) # JSON array of milestones
    current_step_index = Column(Integer, default=0)

    career_goal = relationship("CareerGoal", back_populates="roadmaps")
