# app/models/role.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    """
    مدل نقش‌های کاربری در سیستم.

    Attributes:
        id: شناسه یکتای نقش
        name: نام نقش (مانند: user, admin)
        description: توضیحات نقش (اختیاری)
        users: لیست کاربرانی که این نقش را دارند
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)  # اضافه کردن description

    # رابطه با کاربران
    users = relationship("User", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        """تبدیل شیء نقش به دیکشنری."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_count": len(self.users) if self.users else 0
        }