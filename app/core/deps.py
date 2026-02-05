from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependency برای session دیتابیس."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# تعریف ساده Aliases - همه با پرانتز استفاده شوند
def DBDep() -> Session:
    """Alias برای Depends(get_db)."""
    return Depends(get_db)


def CurrentUser():
    """Alias برای Depends(get_current_user)."""
    from app.core.security import get_current_user
    return Depends(get_current_user)


def AdminDep():
    """Alias برای Depends(get_current_admin)."""
    from app.core.security import get_current_admin
    return Depends(get_current_admin)