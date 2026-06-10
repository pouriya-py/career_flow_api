# app/models.py
from sqlalchemy import Column, Integer, String, JSON, Enum as SQLEnum
from app.database import Base
import enum

# تعریف Enumها در سطح دیتابیس (برای سازگاری بهتر با SQLite از String استفاده می‌کنیم)
class MarketType(str, enum.Enum):
    iran = "IRAN"
    global_market = "GLOBAL"

class JobStatus(str, enum.Enum):
    open = "OPEN"
    closed = "CLOSED"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    # استفاده از JSON برای ذخیره لیست مهارت‌ها (در SQLite مدرن پشتیبانی می‌شود)
    skills = Column(JSON, nullable=False) 
    target_market = Column(SQLEnum(MarketType), default=MarketType.global_market, nullable=False)
    experience_years = Column(Integer, nullable=False)

class JobOpportunity(Base):
    __tablename__ = "job_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    required_skills = Column(JSON, nullable=False)
    market_type = Column(SQLEnum(MarketType), nullable=False)
    url = Column(String(255), nullable=True)
    status = Column(SQLEnum(JobStatus), default=JobStatus.open, nullable=False)