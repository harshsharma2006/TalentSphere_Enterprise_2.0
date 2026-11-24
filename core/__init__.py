"""
TalentSphere Enterprise 2.0 Core Package
"""
from core.config import settings
from core.security import hash_password, verify_password, validate_password_strength
from core.permissions import Role, has_permission, require_role
from core.exceptions import TalentSphereException, AuthenticationError, PermissionDeniedError, EntityNotFoundError, ValidationError
from core.logging import get_logger

__all__ = [
    "settings",
    "hash_password",
    "verify_password",
    "validate_password_strength",
    "Role",
    "has_permission",
    "require_role",
    "TalentSphereException",
    "AuthenticationError",
    "PermissionDeniedError",
    "EntityNotFoundError",
    "ValidationError",
    "get_logger"
]
