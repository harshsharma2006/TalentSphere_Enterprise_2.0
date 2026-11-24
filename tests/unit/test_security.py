"""
Unit tests for Core Security, Password Hashing, and Input Validation
"""

import pytest
from core.security import (
    hash_password,
    verify_password,
    validate_password_strength,
    generate_secure_token
)

def test_password_hashing_and_verification():
    raw_password = "SecurePassword2026!"
    hashed = hash_password(raw_password)
    
    assert hashed != raw_password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_password_strength_validation_valid():
    is_valid, msg = validate_password_strength("StrongPass123!")
    assert is_valid is True
    assert msg == "Strong"

def test_password_strength_validation_too_short():
    is_valid, msg = validate_password_strength("Short1!")
    assert is_valid is False
    assert "at least 8 characters" in msg

def test_password_strength_validation_missing_components():
    # Missing uppercase
    is_valid, _ = validate_password_strength("lowercase123!")
    assert is_valid is False

    # Missing lowercase
    is_valid, _ = validate_password_strength("UPPERCASE123!")
    assert is_valid is False

    # Missing digit
    is_valid, _ = validate_password_strength("NoDigitsHere!")
    assert is_valid is False

    # Missing special char
    is_valid, _ = validate_password_strength("NoSpecialChar123")
    assert is_valid is False

def test_secure_token_generation():
    token1 = generate_secure_token(32)
    token2 = generate_secure_token(32)
    assert len(token1) >= 32
    assert token1 != token2
