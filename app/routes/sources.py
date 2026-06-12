# app/routes/sources.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sources", tags=["Job Sources"])

@router.get("/", response_model=List[schemas.JobSourceResponse])
def get_job_sources(
    skip: int = 0,
    limit: int = 50,
    is_freelance: Optional[bool] = Query(None, description="فقط سایت‌های فریلنسری"),
    is_active: Optional[bool] = Query(None, description="فقط سایت‌های فعال"),
    db: Session = Depends(get_db)
):
    """
    دریافت لیست سایت‌های کاریابی و فریلنسری
    """
    query = db.query(models.JobSource)
    
    if is_freelance is not None:
        query = query.filter(models.JobSource.is_freelance == is_freelance)
    
    if is_active is not None:
        query = query.filter(models.JobSource.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()



@router.get("/active", response_model=List[schemas.JobSourceResponse])
def get_active_job_sources(db: Session = Depends(get_db)):
    """
    دریافت لیست سایت‌های کاریابی فعال (برای اسکرپر)
    """
    return db.query(models.JobSource).filter(
        models.JobSource.is_active == True,
        models.JobSource.is_freelance == False
    ).all()