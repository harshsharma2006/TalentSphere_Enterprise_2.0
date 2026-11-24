"""
Database Engine & Session Management for TalentSphere Enterprise 2.0.
Configures SQLAlchemy connection pooling, SQLite WAL pragma listeners,
and contextual database session generators.
"""
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from core.logging import get_logger
from database.base import Base

logger = get_logger("database")

def _build_engine():
    """Builds and returns configured SQLAlchemy engine."""
    connect_args = {}
    if settings.is_sqlite:
        connect_args = {"check_same_thread": False, "timeout": 30.0}
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args=connect_args,
            echo=False
        )

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.close()
    else:
        # PostgreSQL / Production settings
        engine = create_engine(
            settings.DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False
        )
    return engine

engine = _build_engine()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager yielding a SQLAlchemy session.
    Automatically commits on normal exit and rolls back on unhandled exceptions.
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session rolled back due to error: {e}", exc_info=True)
        raise
    finally:
        session.close()

def init_db() -> None:
    """Creates all registered database tables and ensures initial administrative seeding."""
    from database.models import (
        User, RoleModel, Organization, ActivityLog,
        Department, Employee, Skill, EmployeeSkill,
        Student, StudentSkill,
        PerformanceReview, EmployeeGoal, KPI,
        JobDescription, CandidateApplication, CandidateInterview, JobMatch,
        Resume, ResumeAnalysis,
        Course, CourseEnrollment, Certification,
        CareerRoadmap, CareerGoal,
        Assessment, AssessmentResult,
        Notification, UserNotification
    )
    Base.metadata.create_all(bind=engine)
    logger.info("All SQLAlchemy database tables verified and created successfully.")
