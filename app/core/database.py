# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# تنظیمات دیتابیس
DATABASE_URL = "sqlite:///./basij.db"  # تغییر نام فایل برای مشخص‌تر بودن

# ایجاد engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # برای SQLite ضروری است
    echo=True  # اضافه کردن echo برای دیباگ - در production غیرفعال کنید
)

# ایجاد session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class برای مدل‌ها
Base = declarative_base()


# تابع کمکی برای ایجاد دیتابیس
def create_database():
    """ایجاد همه جداول در دیتابیس"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ دیتابیس در {DATABASE_URL} ایجاد شد")


# تابع کمکی برای دیدن جداول ایجاد شده
def show_tables():
    """نمایش جداول ایجاد شده در دیتابیس"""
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n📊 جداول موجود در دیتابیس:")
    for table in tables:
        print(f"  - {table}")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"    ├─ {column['name']}: {column['type']}")

    return tables