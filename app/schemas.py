from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum


class MarketType(str, Enum):
    IRAN = "IRAN"
    GLOBAL = "GLOBAL"


class UserProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    skills: Optional[List[str]] = Field(default=[])
    target_market: MarketType = Field(default=MarketType.GLOBAL)
    experience_years: int = Field(..., ge=0, le=50)
    email: Optional[EmailStr] = None
    favorite_source_ids: Optional[List[int]] = Field(default=[])


class UserProfileCreate(UserProfileBase):
    password: str = Field(..., min_length=6)


class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    skills: Optional[List[str]] = None
    target_market: Optional[MarketType] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    password: Optional[str] = Field(None, min_length=6)
    favorite_source_ids: Optional[List[int]] = None


class UserProfileResponse(UserProfileBase):
    id: int
    telegram_chat_id: Optional[str] = None
    telegram_activation_code: Optional[str] = None
    is_telegram_verified: bool = False
    favorite_sources: Optional[List['JobSourceResponse']] = []
    
    class Config:
        from_attributes = True


class JobSourceBase(BaseModel):
    name: str
    display_name: str
    base_url: Optional[str] = None
    is_active: bool = True
    is_freelance: bool = False


class JobSourceResponse(JobSourceBase):
    id: int
    
    class Config:
        from_attributes = True


class JobOpportunityBase(BaseModel):
    title: str = Field(..., min_length=3)
    company: str
    required_skills: List[str]
    market_type: MarketType
    url: Optional[str] = None
    source: Optional[str] = None
    is_remote: bool = False


class JobOpportunityCreate(JobOpportunityBase):
    pass


class JobOpportunityResponse(JobOpportunityBase):
    id: int
    status: str = "ACTIVE"
    
    class Config:
        from_attributes = True


class JobOpportunityUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    required_skills: Optional[List[str]] = None
    market_type: Optional[MarketType] = None
    url: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    is_remote: Optional[bool] = None