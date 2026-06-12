# app/models.py
from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum


# تعریف Enum برای نوع بازار
class MarketType(enum.Enum):
    IRAN = "IRAN"
    GLOBAL = "GLOBAL"


# جدول ارتباطی بین کاربر و سایت‌های کاریابی مورد علاقه (Many-to-Many)
user_favorite_sources = Table(
    'user_favorite_sources',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user_profiles.id'), primary_key=True),
    Column('source_id', Integer, ForeignKey('job_sources.id'), primary_key=True)
)


# مدل کاربر
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    skills = Column(JSON, nullable=False)
    target_market = Column(SQLEnum(MarketType), default=MarketType.GLOBAL, nullable=False)
    experience_years = Column(Integer, nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    
    telegram_chat_id = Column(String(50), nullable=True, unique=True)
    telegram_activation_code = Column(String(100), nullable=True, unique=True)
    is_telegram_verified = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    # رابطه Many-to-Many با سایت‌های کاریابی مورد علاقه
    favorite_sources = relationship("JobSource", secondary=user_favorite_sources, backref="favorited_by_users")


# مدل فرصت شغلی
class JobOpportunity(Base):
    __tablename__ = "job_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(100), nullable=False)
    required_skills = Column(JSON, nullable=False)
    market_type = Column(SQLEnum(MarketType), default=MarketType.GLOBAL, nullable=False)
    url = Column(String(500), nullable=True)
    source = Column(String(100), nullable=True)
    is_remote = Column(Boolean, default=False, nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# مدل سایت‌های کاریابی
class JobSource(Base):
    __tablename__ = "job_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_freelance = Column(Boolean, default=False, nullable=False)


# مدل IPهای مسدود شده
class BlockedIP(Base):
    __tablename__ = "blocked_ips"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(50), nullable=False, unique=True)
    reason = Column(String(255), nullable=True)
    blocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)