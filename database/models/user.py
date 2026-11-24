"""
User, Role, Organization, and Activity Log Models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Organization(Base, IDMixin, TimestampMixin):
    """Corporate company, college institution, or school district."""
    __tablename__ = "organizations"

    name = Column(String(150), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    org_type = Column(String(50), default="Corporate") # Corporate, University, High School
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="organization", cascade="all, delete-orphan")

class RoleModel(Base, IDMixin, TimestampMixin):
    """System RBAC Role."""
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

class User(Base, IDMixin, TimestampMixin):
    """User account entity supporting all 6 enterprise roles."""
    __tablename__ = "users"

    email = Column(String(120), unique=True, nullable=False, index=True)
    username = Column(String(60), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(120), nullable=True)
    role = Column(String(50), nullable=False, default="Employee", index=True) # Super Admin, HR Admin, College Admin, Employee, College Student, High School Student
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=False)
    last_login_at = Column(DateTime, nullable=True)

    organization = relationship("Organization", back_populates="users")
    employee_profile = relationship("Employee", back_populates="user", uselist=False, cascade="all, delete-orphan")
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("UserNotification", back_populates="user", cascade="all, delete-orphan")
    career_goals = relationship("CareerGoal", back_populates="user", cascade="all, delete-orphan")
    enrollments = relationship("CourseEnrollment", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")

    @property
    def first_name(self) -> str:
        if self.full_name:
            parts = self.full_name.split()
            return parts[0] if parts else self.username
        return self.username

    @property
    def last_name(self) -> str:
        if self.full_name:
            parts = self.full_name.split()
            return " ".join(parts[1:]) if len(parts) > 1 else ""
        return ""

class ActivityLog(Base, IDMixin, TimestampMixin):
    """Security and compliance audit trail."""
    __tablename__ = "activity_logs"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)

    user = relationship("User", back_populates="activity_logs")
