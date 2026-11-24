"""
Department, Employee, and Employee Skills Models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Department(Base, IDMixin, TimestampMixin):
    """Department / Business Unit."""
    __tablename__ = "departments"

    name = Column(String(100), nullable=False)
    code = Column(String(30), unique=True, nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)

    organization = relationship("Organization", back_populates="departments")
    employees = relationship("Employee", back_populates="department")
    job_descriptions = relationship("JobDescription", back_populates="department")
    kpis = relationship("KPI", back_populates="department")

class Employee(Base, IDMixin, TimestampMixin):
    """Core Employee Record."""
    __tablename__ = "employees"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    designation = Column(String(100), nullable=False)
    employment_type = Column(String(40), default="Full-Time") # Full-Time, Contract, Intern
    years_experience = Column(Float, default=0.0)
    current_salary = Column(Float, nullable=True)
    status = Column(String(30), default="Active") # Active, On Leave, Resigned

    user = relationship("User", back_populates="employee_profile")
    department = relationship("Department", back_populates="employees")
    skills = relationship("EmployeeSkill", back_populates="employee", cascade="all, delete-orphan")
    reviews = relationship("PerformanceReview", back_populates="employee", cascade="all, delete-orphan")
    goals = relationship("EmployeeGoal", back_populates="employee", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

class Skill(Base, IDMixin, TimestampMixin):
    """Standardized skills taxonomy."""
    __tablename__ = "skills"

    name = Column(String(80), unique=True, nullable=False, index=True)
    category = Column(String(50), default="Technical") # Technical, Soft Skills, Leadership, Domain

    employee_skills = relationship("EmployeeSkill", back_populates="skill")
    student_skills = relationship("StudentSkill", back_populates="skill")

class EmployeeSkill(Base, IDMixin, TimestampMixin):
    """Association linking employee to skill with proficiency."""
    __tablename__ = "employee_skills"

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    proficiency_level = Column(String(30), default="Intermediate") # Beginner, Intermediate, Advanced, Expert
    years_experience = Column(Float, default=1.0)
    verified = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="skills")
    skill = relationship("Skill", back_populates="employee_skills")
