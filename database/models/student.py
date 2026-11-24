"""
Student and Student Skills Models for College and High School Portals.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Student(Base, IDMixin, TimestampMixin):
    """Academic Student Profile (College or High School)."""
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    student_code = Column(String(50), unique=True, nullable=False, index=True)
    student_type = Column(String(40), nullable=False) # College Student, High School Student
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    institution_name = Column(String(150), nullable=True)
    degree_program = Column(String(100), nullable=True) # B.Tech, B.Sc, High School Diploma
    major = Column(String(100), nullable=True)
    current_year = Column(Integer, default=1)
    graduation_year = Column(Integer, nullable=True)
    cgpa_percentage = Column(Float, default=0.0)
    placement_status = Column(String(40), default="Seeking") # Eligible, Seeking, Placed

    user = relationship("User", back_populates="student_profile")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

class StudentSkill(Base, IDMixin, TimestampMixin):
    """Association linking student to acquired skill with proficiency."""
    __tablename__ = "student_skills"

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    proficiency_level = Column(String(30), default="Beginner") # Beginner, Intermediate, Advanced

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")
