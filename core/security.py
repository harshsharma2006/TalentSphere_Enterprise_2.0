"""
Security & Cryptography Engine for TalentSphere Enterprise 2.0.
Provides Bcrypt password hashing, complexity validation, and secure token utilities.
"""
import secrets
import bcrypt
from typing import Tuple
from core.config import settings

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validates enterprise password complexity:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special symbol
    """
    if not password or len(password) < 8:
        return False, "Password must contain at least 8 characters."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    special_characters = "@#$%!^&*()_-+=<>?/\\|{}[]~`'\".,:;"
    if not any(c in special_characters for c in password):
        return False, "Password must contain at least one special character."
    return True, "Strong"

def hash_password(password: str) -> str:
    """Hashes a plaintext password using Bcrypt with configured salt rounds."""
    salt = bcrypt.gensalt(rounds=settings.PASSWORD_BCRYPT_ROUNDS)
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Safely verifies a plaintext password against a Bcrypt hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def generate_secure_token(nbytes: int = 32) -> str:
    """Generates a cryptographically secure URL-safe hexadecimal token."""
    return secrets.token_hex(nbytes)
