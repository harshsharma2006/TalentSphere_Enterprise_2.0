"""
SQLAlchemy Base & Declarative Engine for TalentSphere Enterprise 2.0.
Provides standard ID and Timestamp mixins for all entity models.
"""
import warnings
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import declarative_base, declared_attr

# Silence duplicate declarative registration warnings during Streamlit module reloads
warnings.filterwarnings("ignore", category=SAWarning)

class CommonBase:
    """Base model class with reload safety (extend_existing=True) for Streamlit live environments."""
    @declared_attr
    def __table_args__(cls):
        return {"extend_existing": True}

Base = declarative_base(cls=CommonBase)

class TimestampMixin:
    """Provides created_at and updated_at datetime tracking."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class IDMixin:
    """Provides autoincrement primary key."""
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
