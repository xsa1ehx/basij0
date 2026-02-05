# app/models/role.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base  # ایمپورت کردن Base از core


class Role(Base):
    """
    مدل SQLAlchemy برای نگهداری اطلاعات نقش‌ها (مانند Admin, Teacher, Student).
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
