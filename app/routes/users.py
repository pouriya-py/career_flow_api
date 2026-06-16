from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
import secrets

from app.database import get_db
from app import models, schemas
from app.auth import get_password_hash, create_access_token, get_current_user, verify_password
from app.services.email_service import send_welcome_email

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    """ثبت یک پروفایل کاربر جدید"""
    db_user = db.query(models.UserProfile).filter(models.UserProfile.name == user.name).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="کاربری با این نام از قبل ثبت شده است."
        )
    
    activation_code = f"ACT-{secrets.token_hex(4).upper()}"
    favorite_source_ids = user.favorite_source_ids or []
    user_data = user.model_dump(exclude={'favorite_source_ids', 'password'})
    
    new_user = models.UserProfile(
        **user_data,
        telegram_activation_code=activation_code,
        hashed_password=get_password_hash(user.password)
    )
    
    if favorite_source_ids:
        sources = db.query(models.JobSource).filter(models.JobSource.id.in_(favorite_source_ids)).all()
        new_user.favorite_sources = sources
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if new_user.email:
        await send_welcome_email(new_user.email, new_user.name, activation_code)
    
    return new_user


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ورود و دریافت توکن JWT"""
    user = db.query(models.UserProfile).filter(models.UserProfile.name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")
    
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[schemas.UserProfileResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """دریافت لیست کاربران"""
    users = db.query(models.UserProfile).offset(skip).limit(limit).all()
    return users


@router.get("/me", response_model=schemas.UserProfileResponse)
def get_current_user_profile(current_user: models.UserProfile = Depends(get_current_user)):
    """دریافت پروفایل کاربر لاگین شده"""
    return current_user


@router.put("/me", response_model=schemas.UserProfileResponse)
def update_user_profile(
    user_update: schemas.UserProfileUpdate,
    current_user: models.UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """آپدیت پروفایل کاربر"""
    update_data = user_update.model_dump(exclude_unset=True)
    
    if 'password' in update_data:
        current_user.hashed_password = get_password_hash(update_data.pop('password'))
    
    if 'favorite_source_ids' in update_data:
        favorite_source_ids = update_data.pop('favorite_source_ids')
        if favorite_source_ids:
            sources = db.query(models.JobSource).filter(models.JobSource.id.in_(favorite_source_ids)).all()
            current_user.favorite_sources = sources
        else:
            current_user.favorite_sources = []
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user