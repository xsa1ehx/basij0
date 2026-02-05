from fastapi import Request
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional

from app.models.audit_log import AuditLog
from app.models.user import User


# ۱. ایجاد لاگ
def create_audit_log(
        db: Session,
        action: str,
        request: Request,
        user: User | None = None,
        entity: str | None = None,
        entity_id: int | None = None,
        description: str | None = None,
):
    """ایجاد یک لاگ جدید"""
    log = AuditLog(
        user_id=user.id if user else None,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description,
        ip_address=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()


# ۲. آمار ساده
def get_simple_audit_stats(db: Session) -> Dict:
    """آمار ساده لاگ‌ها"""
    total_logs = db.query(AuditLog).count()

    actions = (
        db.query(AuditLog.action, func.count(AuditLog.id))
        .group_by(AuditLog.action)
        .all()
    )

    actions_dict: Dict[str, int] = {
        action: count for action, count in actions
    }

    return {
        "total_logs": total_logs,
        "actions": actions_dict,
    }


# ۳. لیست لاگ‌ها با تاریخ و ساعت
def get_audit_logs(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        action: Optional[str] = None,
        user_id: Optional[int] = None,
) -> Dict:
    """
    دریافت لیست لاگ‌ها با تاریخ و ساعت

    Returns:
        {
            "logs": List[AuditLog],  # لیست لاگ‌ها
            "total": int,            # تعداد کل لاگ‌ها
            "skip": int,             # تعداد رد شده
            "limit": int,            # تعداد نمایش داده شده
            "has_more": bool         # آیا لاگ بیشتری وجود دارد؟
        }
    """
    query = db.query(AuditLog)

    # فیلترها
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    # تعداد کل
    total = query.count()

    # دریافت لاگ‌ها با مرتب‌سازی بر اساس تاریخ و ساعت (جدیدترین اول)
    logs = (
        query
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "logs": logs,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total,
    }


# ۴. تابع کمکی برای فرمت تاریخ در template
def format_datetime(dt: datetime) -> str:
    """فرمت کردن تاریخ برای نمایش"""
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")



