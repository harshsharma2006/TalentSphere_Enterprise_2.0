"""
Performance Review, KPI, and Goal Management Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class KPI(Base, IDMixin, TimestampMixin):
    """Departmental or organizational Key Performance Indicator."""
    __tablename__ = "kpis"

    title = Column(String(120), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String(30), default="%")

    department = relationship("Department", back_populates="kpis")

class EmployeeGoal(Base, IDMixin, TimestampMixin):
    """Assigned developmental or delivery goal."""
    __tablename__ = "employee_goals"

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="Technical")
    due_date = Column(Date, nullable=True)
    status = Column(String(30), default="In Progress") # Pending, In Progress, Achieved, Cancelled
    progress_pct = Column(Integer, default=0)

    employee = relationship("Employee", back_populates="goals")

class PerformanceReview(Base, IDMixin, TimestampMixin):
    """Quantitative and qualitative performance appraisal."""
    __tablename__ = "performance_reviews"

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_period = Column(String(50), default="Annual")
    overall_rating = Column(Float, nullable=False) # 1.0 to 5.0
    technical_rating = Column(Float, default=3.0)
    leadership_rating = Column(Float, default=3.0)
    communication_rating = Column(Float, default=3.0)
    achievements = Column(Text, nullable=False)
    growth_areas = Column(Text, nullable=False)
    reviewer_name = Column(String(100), default="HR Manager")

    employee = relationship("Employee", back_populates="reviews")
