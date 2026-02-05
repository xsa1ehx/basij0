# scripts/run.py
import uvicorn
import sys
import os

if __name__ == "__main__":
    # اضافه کردن مسیر پروژه
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # اجرای سرور
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )