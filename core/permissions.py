"""
Role-Based Access Control (RBAC) and Permissions for TalentSphere Enterprise 2.0.
Defines the six core enterprise roles and provides server-side authorization enforcement.
"""
from enum import Enum
from typing import Set, Dict, List, Union
from core.exceptions import PermissionDeniedError

class Role(str, Enum):
    SUPER_ADMIN = "Super Admin"
    HR_ADMIN = "HR Admin"
    COLLEGE_ADMIN = "College Admin"
    EMPLOYEE = "Employee"
    COLLEGE_STUDENT = "College Student"
    HIGH_SCHOOL_STUDENT = "High School Student"

# Permission tokens
class Permission(str, Enum):
    # Platform Governance
    SYSTEM_CONFIG = "system:config"
    MANAGE_ORGANIZATIONS = "manage:organizations"
    MANAGE_ALL_USERS = "manage:all_users"
    VIEW_AUDIT_LOGS = "view:audit_logs"

    # HR & Workforce Management
    MANAGE_EMPLOYEES = "manage:employees"
    VIEW_EMPLOYEES = "view:employees"
    MANAGE_PERFORMANCE_REVIEWS = "manage:performance_reviews"
    VIEW_PERFORMANCE_REVIEWS = "view:performance_reviews"
    MANAGE_RECRUITMENT = "manage:recruitment"
    MANAGE_COURSES = "manage:courses"
    VIEW_WORKFORCE_ANALYTICS = "view:workforce_analytics"

    # College & Academic Management
    MANAGE_STUDENTS = "manage:students"
    VIEW_STUDENTS = "view:students"
    MANAGE_PLACEMENTS = "manage:placements"
    VIEW_ACADEMIC_ANALYTICS = "view:academic_analytics"

    # Employee Self-Service
    VIEW_OWN_PROFILE = "view:own_profile"
    EDIT_OWN_PROFILE = "edit:own_profile"
    VIEW_OWN_REVIEWS = "view:own_reviews"
    MANAGE_CAREER_GOALS = "manage:career_goals"
    ENROLL_COURSES = "enroll:courses"

    # Student Self-Service
    ASSESS_SKILLS = "assess:skills"
    ANALYZE_RESUME = "analyze:resume"
    ACCESS_INTERVIEW_PREP = "access:interview_prep"
    VIEW_CAREER_EXPLORER = "view:career_explorer"

# Role to Permissions matrix
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.SUPER_ADMIN: set(Permission),  # Super Admin has all permissions
    
    Role.HR_ADMIN: {
        Permission.MANAGE_EMPLOYEES,
        Permission.VIEW_EMPLOYEES,
        Permission.MANAGE_PERFORMANCE_REVIEWS,
        Permission.VIEW_PERFORMANCE_REVIEWS,
        Permission.MANAGE_RECRUITMENT,
        Permission.MANAGE_COURSES,
        Permission.VIEW_WORKFORCE_ANALYTICS,
        Permission.ANALYZE_RESUME,
        Permission.VIEW_OWN_PROFILE,
        Permission.EDIT_OWN_PROFILE
    },

    Role.COLLEGE_ADMIN: {
        Permission.MANAGE_STUDENTS,
        Permission.VIEW_STUDENTS,
        Permission.MANAGE_PLACEMENTS,
        Permission.VIEW_ACADEMIC_ANALYTICS,
        Permission.MANAGE_COURSES,
        Permission.ANALYZE_RESUME,
        Permission.VIEW_OWN_PROFILE,
        Permission.EDIT_OWN_PROFILE
    },

    Role.EMPLOYEE: {
        Permission.VIEW_OWN_PROFILE,
        Permission.EDIT_OWN_PROFILE,
        Permission.VIEW_OWN_REVIEWS,
        Permission.MANAGE_CAREER_GOALS,
        Permission.ENROLL_COURSES,
        Permission.ANALYZE_RESUME,
        Permission.ASSESS_SKILLS
    },

    Role.COLLEGE_STUDENT: {
        Permission.VIEW_OWN_PROFILE,
        Permission.EDIT_OWN_PROFILE,
        Permission.ASSESS_SKILLS,
        Permission.ANALYZE_RESUME,
        Permission.ACCESS_INTERVIEW_PREP,
        Permission.ENROLL_COURSES,
        Permission.MANAGE_CAREER_GOALS,
        Permission.VIEW_CAREER_EXPLORER
    },

    Role.HIGH_SCHOOL_STUDENT: {
        Permission.VIEW_OWN_PROFILE,
        Permission.EDIT_OWN_PROFILE,
        Permission.VIEW_CAREER_EXPLORER,
        Permission.ASSESS_SKILLS,
        Permission.ENROLL_COURSES,
        Permission.MANAGE_CAREER_GOALS
    }
}

def has_permission(user_role: Union[str, Role], permission: Union[Permission, str]) -> bool:
    """Checks whether a given user role possesses the requested permission."""
    try:
        role_enum = Role(user_role)
    except ValueError:
        return False

    perm_enum = None
    if isinstance(permission, Permission):
        perm_enum = permission
    elif isinstance(permission, str):
        # Match by value or enum name
        for p in Permission:
            if p.value == permission or p.name.lower() == permission.lower() or p.value.replace(":", "_") == permission:
                perm_enum = p
                break

    if not perm_enum:
        return False

    return perm_enum in ROLE_PERMISSIONS.get(role_enum, set())

def require_role(user_role: Union[str, Role], allowed_roles: List[Union[Role, str]]) -> None:
    """Raises PermissionDeniedError if user does not possess one of the allowed roles."""
    normalized_allowed = [str(r.value if isinstance(r, Role) else r) for r in allowed_roles]
    current_role_str = str(user_role.value if isinstance(user_role, Role) else user_role)
    if current_role_str not in normalized_allowed:
        raise PermissionDeniedError(
            f"Action forbidden. Role '{current_role_str}' lacks required role permission ({', '.join(normalized_allowed)})."
        )
