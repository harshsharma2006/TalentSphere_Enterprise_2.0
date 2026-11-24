"""
Custom Exceptions for TalentSphere Enterprise 2.0.
"""

class TalentSphereException(Exception):
    """Base exception for all TalentSphere errors."""
    def __init__(self, message: str = "An unexpected error occurred in TalentSphere."):
        super().__init__(message)
        self.message = message

class AuthenticationError(TalentSphereException):
    """Raised when authentication fails."""
    pass

class PermissionDeniedError(TalentSphereException):
    """Raised when an authenticated user attempts an unauthorized action."""
    pass

class EntityNotFoundError(TalentSphereException):
    """Raised when a requested database entity does not exist."""
    def __init__(self, entity_name_or_msg: str, identifier: any = None):
        if identifier is not None:
            msg = f"{entity_name_or_msg} with identifier '{identifier}' was not found."
        else:
            msg = entity_name_or_msg
        super().__init__(msg)
        self.entity_name = entity_name_or_msg
        self.identifier = identifier

class ValidationError(TalentSphereException):
    """Raised when input validation fails."""
    def __init__(self, field_or_msg: str, reason: str = None):
        if reason is not None:
            msg = f"Validation failed for '{field_or_msg}': {reason}"
        else:
            msg = field_or_msg
        super().__init__(msg)
        self.field = field_or_msg
        self.reason = reason

class AIProcessingError(TalentSphereException):
    """Raised when AI engine or document parsing encounters a failure."""
    pass

# Aliases for consistent naming across enterprise modules
AuthenticationException = AuthenticationError
PermissionException = PermissionDeniedError
NotFoundException = EntityNotFoundError
ValidationException = ValidationError
