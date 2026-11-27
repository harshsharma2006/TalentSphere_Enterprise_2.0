"""
Pytest configuration and test fixtures for TalentSphere Enterprise 2.0
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.session import init_db, get_db_session
from database.models.user import User, Organization
from core.security import hash_password
from core.permissions import Role

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure all database schema tables exist and enterprise seed data is loaded."""
    init_db()
    from scripts.seed_database import seed_enterprise_data
    seed_enterprise_data()
    yield

@pytest.fixture
def db():
    """Provides a transactional database session for tests."""
    with get_db_session() as session:
        yield session
