"""
Notification and User Notification Dispatch Models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base, TimestampMixin, IDMixin

class Notification(Base, IDMixin, TimestampMixin):
    """Platform-wide or group broadcast notification."""
    __tablename__ = "notifications"

    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    target_group = Column(String(50), default="All") # All, Employee, College Student, High School Student, Super Admin
    sender_name = Column(String(100), default="System")

    user_dispatches = relationship("UserNotification", back_populates="notification", cascade="all, delete-orphan")

class UserNotification(Base, IDMixin, TimestampMixin):
    """Personal Inbox Notification for a User."""
    __tablename__ = "user_notifications"

    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    notification = relationship("Notification", back_populates="user_dispatches")
    user = relationship("User", back_populates="notifications")
