from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import get_current_admin
from app.schemas.student import StudentProfileOut, AdminStudentUpdate
from app.services import user_service
from app.services.user_service import _check_uniqueness  # import صحیح تابع

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)],
)

@router.get("/students", response_model=list[StudentProfileOut])
def list_students(db: Session = Depends(get_db)):
    return user_service.get_all_students(db)

@router.get("/students/{student_id}", response_model=StudentProfileOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return user_service.get_student_by_id(db, student_id)

@router.put("/students/{student_id}", response_model=StudentProfileOut)
def update_student(
        student_id: int,
        data: AdminStudentUpdate,
        db: Session = Depends(get_db),
):
    # چک کردن تکراری بودن شماره دانشجویی و کد ملی
    _check_uniqueness(
        db,
        national_code=data.national_code,
        student_number=data.student_number,
        exclude_user_id=student_id
    )

    return user_service.admin_update_student(db, student_id, data)

