# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import secrets
from app.services.email_service import send_welcome_email

from app.database import get_db
from app import models, schemas

# ساخت روتر با پیشوند و تگ برای دسته‌بندی در مستندات Swagger
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    """
    ثبت یک پروفایل کاربر جدید با مهارت‌ها و بازار هدف.
    """
    # بررسی تکراری نبودن نام (یک اعتبارسنجی ساده)
    db_user = db.query(models.UserProfile).filter(models.UserProfile.name == user.name).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="کاربری با این نام از قبل ثبت شده است."
        )
        
    import secrets
    
    # تبدیل داده‌های Pydantic به مدل SQLAlchemy و ذخیره در دیتابیس
    # نکته: در Pydantic v2 از model_dump() به جای dict() استفاده می‌کنیم
    
    activation_code = f"ACT-{secrets.token_hex(4).upper()}"
    new_user = models.UserProfile(
        **user.model_dump(), 
        telegram_activation_code=activation_code
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # به‌روزرسانی آبجکت با ID تولید شده توسط دیتابیس
    
    
    if new_user.email:
        email_result = await send_welcome_email(
            user_email=new_user.email,
            user_name=new_user.name,
            activation_code=activation_code
        )
        
        # می‌توانیم نتیجه را در لاگ ببینیم
        print(f"📧 Email Result: {email_result}")
        
          
    return new_user

@router.get("/", response_model=List[schemas.UserProfileResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    دریافت لیست کاربران ثبت‌شده (با قابلیت صفحه‌بندی).
    """
    users = db.query(models.UserProfile).offset(skip).limit(limit).all()
    return users