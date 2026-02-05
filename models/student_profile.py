# app/models/student_profile.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base  # ایمپورت کردن Base از core


class StudentProfile(Base):
    """
    مدل SQLAlchemy برای نگهداری پروفایل اختصاصی دانشجویان (رابطه One-to-One با User).
    """
    __tablename__ = "student_profiles"

    # user_id هم به عنوان کلید اصلی (PK) و هم کلید خارجی (FK) عمل می‌کند (برای One-to-One)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    student_number = Column(String(20), unique=True, index=True, nullable=True)

    # تعریف رابطه One-to-One با مدل User
    user = relationship(
        "User",
        back_populates="student_profile"
    )

    def __repr__(self):
        return f"<StudentProfile(user_id={self.user_id}, student_number='{self.student_number}')>"
