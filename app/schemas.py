# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# تعریف یک Enum برای بازار هدف (استانداردسازی داده‌ها)
class MarketType(str, Enum):
    iran = "IRAN"
    global_market = "GLOBAL"

class JobStatus(str, Enum):
    open = "OPEN"
    closed = "CLOSED"

# --- مدل‌های مربوط به کاربر ---
class UserProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="نام کاربر")
    skills: List[str] = Field(..., description="لیست مهارت‌ها (مثلاً: ['Python', 'FastAPI'])")
    target_market: MarketType = Field(default=MarketType.global_market, description="بازار هدف: IRAN یا GLOBAL")
    experience_years: int = Field(..., ge=0, le=50, description="سال‌های تجربه")

class UserProfileCreate(UserProfileBase):
    pass # در آینده می‌توانیم فیلدهای خاصی برای ساخت اضافه کنیم

class UserProfileResponse(UserProfileBase):
    id: int
    
    class Config:
        from_attributes = True # معادل orm_mode در Pydantic v2

# --- مدل‌های مربوط به شغل ---
class JobOpportunityBase(BaseModel):
    title: str = Field(..., min_length=3, description="عنوان شغلی")
    company: str = Field(..., description="نام شرکت")
    required_skills: List[str] = Field(..., description="مهارت‌های مورد نیاز")
    market_type: MarketType = Field(..., description="بازار این شغل")
    url: Optional[str] = Field(None, description="لینک آگهی شغلی")
    status: JobStatus = Field(default=JobStatus.open)

class JobOpportunityCreate(JobOpportunityBase):
    pass

class JobOpportunityResponse(JobOpportunityBase):
    id: int
    
    class Config:
        from_attributes = True
        
        
        
class JobOpportunityUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    required_skills: Optional[List[str]] = None
    market_type: Optional[MarketType] = None
    url: Optional[str] = None
    status: Optional[JobStatus] = None