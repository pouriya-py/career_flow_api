# app/routes/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=schemas.JobOpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_job_opportunity(job: schemas.JobOpportunityCreate, db: Session = Depends(get_db)):
    """
    ثبت یک فرصت شغلی جدید.
    """
    db_job = models.JobOpportunity(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[schemas.JobOpportunityResponse])
def get_all_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    دریافت لیست تمام فرصت‌های شغلی.
    """
    return db.query(models.JobOpportunity).offset(skip).limit(limit).all()

# ✨✨✨ بخش هیجان‌انگیز: الگوریتم پیشنهاد شغل ✨✨✨
@router.get("/match/{user_id}", response_model=List[Dict[str, Any]])
def match_jobs_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    پیدا کردن شغل‌های مناسب برای یک کاربر بر اساس تطابق مهارت‌ها.
    """
    # ۱. پیدا کردن کاربر
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_skills = set(user.skills)
    if not user_skills:
        return {"message": "User has no skills defined."}

    # ۲. دریافت تمام شغل‌های باز (Open)
    open_jobs = db.query(models.JobOpportunity).filter(
        models.JobOpportunity.status == models.JobStatus.open
    ).all()
    
    matched_jobs = []
    
    # ۳. محاسبه درصد تطابق برای هر شغل
    for job in open_jobs:
        job_skills = set(job.required_skills)
        
        # پیدا کردن مهارت‌های مشترک (اشتراک دو مجموعه)
        common_skills = user_skills.intersection(job_skills)
        
        if common_skills:
            # محاسبه درصد تطابق (چند درصد از مهارت‌های شغل را کاربر دارد؟)
            match_percentage = (len(common_skills) / len(job_skills)) * 100
            
            matched_jobs.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "market_type": job.market_type.value,
                "match_percentage": round(match_percentage, 2),
                "your_matching_skills": list(common_skills)
            })
    
    # ۴. مرتب‌سازی لیست از بیشترین درصد تطابق به کمترین
    matched_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return matched_jobs