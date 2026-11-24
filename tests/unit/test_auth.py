"""
Unit tests for Authentication Service and Role Permissions
"""

import pytest
from services.auth_service import AuthService
from core.permissions import Role, Permission, has_permission
from core.exceptions import AuthenticationError

def test_superadmin_authentication_success():
    auth_res = AuthService.authenticate("superadmin", "SuperAdmin@2026")
    assert auth_res is not None
    assert auth_res["username"] == "superadmin"
    assert auth_res["role"] == Role.SUPER_ADMIN.value

def test_authentication_invalid_credentials():
    with pytest.raises(AuthenticationError):
        AuthService.authenticate("superadmin", "WrongPassword123!")

def test_authentication_nonexistent_user():
    with pytest.raises(AuthenticationError):
        AuthService.authenticate("nonexistent_user_xyz", "SomePassword123!")

def test_role_permission_matrix():
    assert has_permission(Role.SUPER_ADMIN.value, Permission.MANAGE_ALL_USERS) is True
    assert has_permission(Role.SUPER_ADMIN.value, "manage:all_users") is True
    assert has_permission(Role.EMPLOYEE.value, Permission.MANAGE_ALL_USERS) is False
    assert has_permission(Role.EMPLOYEE.value, Permission.VIEW_OWN_PROFILE) is True
    assert has_permission(Role.COLLEGE_STUDENT.value, Permission.ASSESS_SKILLS) is True
    assert has_permission(Role.HIGH_SCHOOL_STUDENT.value, Permission.VIEW_CAREER_EXPLORER) is True
