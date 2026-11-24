"""
SQLAlchemy Base & Declarative Engine for TalentSphere Enterprise 2.0.
Provides standard ID and Timestamp mixins for all entity models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()

class TimestampMixin:
    """Provides created_at and updated_at datetime tracking."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class IDMixin:
    """Provides autoincrement primary key."""
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
