from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.models.audit_log import AuditLog
from app.models.user import User  # فرض می‌کنیم مدل User اینجا است

# ایجاد router
router = APIRouter()


@router.get("/audit-logs", response_class=HTMLResponse)
def audit_logs_page(
    request: Request,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
    # پارامترهای query (فیلترها)
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
):
    query = db.query(AuditLog)

    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action == action)

    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)

    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)

    logs = (
        query
        .order_by(AuditLog.created_at.desc())
        .limit(500)
        .all()
    )

    # اضافه کردن اطلاعات شماره دانشجویی و کد ملی
    for log in logs:
        if log.user:
            log.student_number = log.user.student_number  # شماره دانشجویی
            log.national_code = log.user.profile.national_code if log.user.profile else None  # کد ملی

    # تبدیل تاریخ‌ها به string برای نمایش در فرم
    date_from_str = date_from.isoformat() if date_from else ""
    date_to_str = date_to.isoformat() if date_to else ""

    return request.app.state.templates.TemplateResponse(
        "admin/audit_logs.html",
        {
            "request": request,
            "logs": logs,
            "filters": {
                "user_id": user_id or "",
                "action": action or "",
                "date_from": date_from_str,
                "date_to": date_to_str,
            },
        },
    )
