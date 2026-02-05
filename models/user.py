

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base  # ایمپورت کردن Base از core


class UserRole(Base):
    """
    جدول میانی برای پیاده‌سازی رابطه Many-to-Many بین User و Role.
    """
    __tablename__ = "user_roles"

    # برای اینکه یک کلید اولیه ترکیبی (Composite Primary Key) باشد
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)

class User(Base):
    """
    مدل SQLAlchemy برای نگهداری اطلاعات کاربران سیستم.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # فیلدهای احراز هویت
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # اطلاعات زمانی
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # رابطه با StudentProfile (One-to-One)
    student_profile = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,  # نشان می‌دهد که این یک رابطه One-to-One است
        cascade="all, delete-orphan"
    )

    roles = relationship(
        "Role",
        secondary=UserRole.__tablename__,  # استفاده از نام جدول میانی
        backref="users"  # امکان دسترسی به کاربران یک نقش: role.users
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
