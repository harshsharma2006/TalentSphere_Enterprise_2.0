"""
Authentication Domain Service for TalentSphere Enterprise 2.0.
Handles secure multi-role login, account registration, forced password changes,
session token tracking, and RBAC user provisioning.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from database.session import get_db_session
from database.models import User, Organization, ActivityLog
from core.security import hash_password, verify_password, validate_password_strength, generate_secure_token
from core.permissions import Role
from core.exceptions import AuthenticationError, ValidationError, EntityNotFoundError
from core.logging import get_logger

logger = get_logger("auth_service")

class AuthService:
    @staticmethod
    def authenticate(username_or_email: str, password: str, client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Authenticates a user against any of the 6 enterprise roles.
        Enforces active status check and updates last_login_at.
        """
        ident = (username_or_email or "").strip().lower()
        if not ident or not password:
            raise AuthenticationError("Username/Email and Password are required.")

        with get_db_session() as session:
            user = session.query(User).filter(
                (User.email.ilike(ident)) | (User.username.ilike(ident))
            ).first()

            if not user:
                logger.warning(f"Authentication failed: User identifier '{ident}' not found.")
                raise AuthenticationError("Invalid credentials provided.")

            if not user.is_active:
                logger.warning(f"Authentication rejected: User '{ident}' is deactivated.")
                raise AuthenticationError("This user account has been deactivated. Please contact an administrator.")

            if not verify_password(password, user.password_hash):
                logger.warning(f"Authentication failed: Incorrect password for '{ident}'.")
                raise AuthenticationError("Invalid credentials provided.")

            # Update last login timestamp
            user.last_login_at = datetime.utcnow()

            # Audit log entry
            session.add(ActivityLog(
                user_id=user.id,
                action="USER_LOGIN",
                details=f"User '{user.username}' successfully signed in with role '{user.role}'.",
                ip_address=client_ip
            ))

            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name or f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username,
                "role": user.role,
                "organization_id": user.organization_id,
                "must_change_password": bool(user.must_change_password),
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
            }

            logger.info(f"User '{user.username}' ({user.role}) authenticated successfully.")
            return user_data

    @staticmethod
    def register_user(
        username: str,
        email: str,
        password: str,
        role: str = Role.EMPLOYEE.value,
        first_name: str = "",
        last_name: str = "",
        phone: str = "",
        organization_id: Optional[int] = None,
        must_change_password: bool = False,
        full_name: str = ""
    ) -> Dict[str, Any]:
        """Registers a new user into the database."""
        u_clean = (username or "").strip().lower()
        e_clean = (email or "").strip().lower()

        if not u_clean or len(u_clean) < 3:
            raise ValidationError("username", "Username must contain at least 3 characters.")

        if "@" not in e_clean or "." not in e_clean:
            raise ValidationError("email", "Please enter a valid email address.")

        # Role validation
        valid_roles = [r.value for r in Role]
        if role not in valid_roles:
            raise ValidationError("role", f"Invalid role specified. Must be one of: {', '.join(valid_roles)}")

        is_strong, msg = validate_password_strength(password)
        if not is_strong:
            raise ValidationError("password", msg)

        display_name = full_name or f"{first_name} {last_name}".strip() or u_clean

        with get_db_session() as session:
            # Check uniqueness
            if session.query(User).filter(User.username.ilike(u_clean)).first():
                raise ValidationError("username", f"Username '{u_clean}' is already registered.")

            if session.query(User).filter(User.email.ilike(e_clean)).first():
                raise ValidationError("email", f"Email '{e_clean}' is already registered.")

            new_user = User(
                username=u_clean,
                email=e_clean,
                password_hash=hash_password(password),
                full_name=display_name,
                role=role,
                organization_id=organization_id,
                is_active=True,
                must_change_password=must_change_password
            )
            session.add(new_user)
            session.flush()
            user_id = new_user.id

            session.add(ActivityLog(
                user_id=user_id,
                action="USER_REGISTERED",
                details=f"New user '{u_clean}' provisioned with role '{role}'."
            ))

        logger.info(f"New user registered: {u_clean} (ID: {user_id}, Role: {role})")
        return {"id": user_id, "username": u_clean, "email": e_clean, "role": role}

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Allows an authenticated user to change their password."""
        is_strong, msg = validate_password_strength(new_password)
        if not is_strong:
            return False, msg

        with get_db_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False, "User not found."

            if not verify_password(old_password, user.password_hash):
                return False, "Current password is incorrect."

            user.password_hash = hash_password(new_password)
            user.must_change_password = False

            session.add(ActivityLog(
                user_id=user.id,
                action="PASSWORD_CHANGED",
                details=f"User '{user.username}' changed their password."
            ))

        logger.info(f"Password changed for user ID #{user_id}.")
        return True, "Password updated successfully."

    @staticmethod
    def force_password_update(user_id: int, new_password: str) -> Tuple[bool, str]:
        """Forces password update upon initial login with default credentials."""
        is_strong, msg = validate_password_strength(new_password)
        if not is_strong:
            return False, msg

        with get_db_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False, "User not found."

            user.password_hash = hash_password(new_password)
            user.must_change_password = False

            session.add(ActivityLog(
                user_id=user.id,
                action="FORCED_PASSWORD_UPDATE",
                details=f"User '{user.username}' updated initial default password."
            ))

        logger.info(f"Forced password update completed for user #{user_id}.")
        return True, "Initial password successfully updated."

    @staticmethod
    def list_users(role_filter: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists users with optional role and keyword search filtering."""
        with get_db_session() as session:
            query = session.query(User)
            if role_filter and role_filter != "All":
                query = query.filter(User.role == role_filter)

            if search:
                s_pat = f"%{search.strip().lower()}%"
                query = query.filter(
                    (User.username.ilike(s_pat)) | (User.email.ilike(s_pat)) | (User.full_name.ilike(s_pat))
                )

            users = query.order_by(User.created_at.desc()).all()
            return [
                {
                    "id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "full_name": u.full_name or f"{u.first_name or ''} {u.last_name or ''}".strip() or u.username,
                    "role": u.role,
                    "is_active": u.is_active,
                    "last_login_at": u.last_login_at.strftime("%Y-%m-%d %H:%M") if u.last_login_at else "Never",
                    "created_at": u.created_at.strftime("%Y-%m-%d") if u.created_at else ""
                }
                for u in users
            ]

    @staticmethod
    def toggle_user_active_status(user_id: int) -> Dict[str, Any]:
        """Activates or deactivates a user account."""
        with get_db_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise EntityNotFoundError("User", user_id)

            user.is_active = not user.is_active
            new_status = user.is_active

            session.add(ActivityLog(
                user_id=user.id,
                action="USER_STATUS_TOGGLED",
                details=f"User '{user.username}' status set to {'Active' if new_status else 'Deactivated'}."
            ))

        logger.info(f"User #{user_id} active status set to {new_status}.")
        return {"id": user_id, "is_active": new_status}

# Module-level convenience functions
authenticate = AuthService.authenticate
register_user = AuthService.register_user
change_password = AuthService.change_password
force_password_update = AuthService.force_password_update
list_users = AuthService.list_users
toggle_user_active_status = AuthService.toggle_user_active_status
