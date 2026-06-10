# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# خواندن آدرس دیتابیس از متغیرهای محیطی (با مقدار پیش‌فرض SQLite)
# در آینده می‌توانیم این را به PostgreSQL تغییر دهیم بدون تغییر در کد
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_flow.db")

# ساخت موتور دیتابیس (Engine)
# connect_args={"check_same_thread": False} فقط برای SQLite لازم است
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# ساخت کارخانه Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# کلاس پایه برای تمام مدل‌های دیتابیس
Base = declarative_base()

# تابع Dependency برای دریافت Session در هر درخواست (بعداً در main.py استفاده می‌کنیم)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()