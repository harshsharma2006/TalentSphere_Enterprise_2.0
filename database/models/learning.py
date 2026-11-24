"""
Learning Course, Course Enrollment, and Certification Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Course(Base, IDMixin, TimestampMixin):
    """Learning Catalog Course."""
    __tablename__ = "courses"

    title = Column(String(150), nullable=False, index=True)
    category = Column(String(60), default="Technical")
    description = Column(Text, nullable=False)
    duration_hours = Column(Integer, default=10)
    difficulty_level = Column(String(30), default="Intermediate") # Beginner, Intermediate, Advanced
    syllabus = Column(Text, nullable=True)
    target_skills = Column(String(255), nullable=True)

    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")

class CourseEnrollment(Base, IDMixin, TimestampMixin):
    """User Course Enrollment & Progress Tracking."""
    __tablename__ = "course_enrollments"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), default="In Progress") # Enrolled, In Progress, Completed
    progress_pct = Column(Integer, default=0) # 0 to 100
    enrolled_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    course = relationship("Course", back_populates="enrollments")
    user = relationship("User", back_populates="enrollments")
    certificate = relationship("Certification", back_populates="enrollment", uselist=False, cascade="all, delete-orphan")

class Certification(Base, IDMixin, TimestampMixin):
    """Verified Course Completion Certificate."""
    __tablename__ = "certifications"

    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id", ondelete="CASCADE"), unique=True, nullable=False)
    certificate_code = Column(String(60), unique=True, nullable=False, index=True)
    certificate_name = Column(String(150), nullable=False)
    issued_date = Column(DateTime, nullable=False)

    enrollment = relationship("CourseEnrollment", back_populates="certificate")
