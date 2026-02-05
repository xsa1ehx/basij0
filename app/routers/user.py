from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_current_admin
from app.core.deps import get_db
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ------------------------------------------------------------------
# دریافت اطلاعات کاربر فعلی (فقط خود کاربر)
# ------------------------------------------------------------------

@router.get("/me", response_model=UserOut)
def read_user_me(
        current_user: User = Depends(get_current_user),  # استفاده از get_current_user برای اعتبارسنجی
):
    """
    دریافت اطلاعات هویتی کاربر فعلی.
    (اطلاعات سیستمی – نه پروفایل دانشجویی)
    """
    return current_user


# ------------------------------------------------------------------
# دریافت اطلاعات یک کاربر خاص (فقط ادمین)
# ------------------------------------------------------------------

@router.get("/{user_id}", response_model=UserOut)
def read_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    دریافت اطلاعات هویتی یک کاربر خاص.
    دسترسی فقط برای ادمین.
    """
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی غیرمجاز",
        )

    # جستجو با استفاده از شماره دانشجویی
    user = db.query(User).filter(User.id == user_id).first()  # فرض بر این است که ID در اینجا موجود است.

    # اگر بخواهیم جستجو را بر اساس شماره دانشجویی یا کد ملی انجام دهیم، می‌توانیم به شکل زیر عمل کنیم:
    # user = db.query(User).filter(User.student_number == "some_student_number").first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر یافت نشد",
        )

    return user
