# app/routes/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# ۱. دریافت لیست شغل‌ها با قابلیت فیلتر و جستجو
# در app/routes/jobs.py، پارامترهای تابع get_jobs را آپدیت کن:
@router.get("/", response_model=List[schemas.JobOpportunityResponse])
def get_jobs(
    skip: int = 0,
    limit: int = 50,
    market_type: Optional[schemas.MarketType] = Query(None, description="فیلتر بر اساس بازار (IRAN یا GLOBAL)"),
    search: Optional[str] = Query(None, description="جستجو در عنوان شغل یا نام شرکت"),
    status_filter: Optional[schemas.JobStatus] = Query(None, alias="status", description="فیلتر بر اساس وضعیت"),
    source: Optional[str] = Query(None, description="فیلتر بر اساس منبع (مثلاً Jobinja, LinkedIn)"),
    is_remote: Optional[bool] = Query(None, description="فقط شغل‌های دورکاری"),
    db: Session = Depends(get_db)
):
    query = db.query(models.JobOpportunity)
    
    if market_type:
        query = query.filter(models.JobOpportunity.market_type == market_type)
    if status_filter:
        query = query.filter(models.JobOpportunity.status == status_filter)
    if source:
        query = query.filter(models.JobOpportunity.source.ilike(f"%{source}%"))
    if is_remote is not None:
        query = query.filter(models.JobOpportunity.is_remote == is_remote)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.JobOpportunity.title.ilike(search_term)) | 
            (models.JobOpportunity.company.ilike(search_term))
        )
    
    return query.offset(skip).limit(limit).all()
    query = db.query(models.JobOpportunity)
    
    # اعمال فیلتر بازار
    if market_type:
        query = query.filter(models.JobOpportunity.market_type == market_type)
    
    # اعمال فیلتر وضعیت
    if status_filter:
        query = query.filter(models.JobOpportunity.status == status_filter)
        
    # اعمال جستجوی متنی (Case-insensitive)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.JobOpportunity.title.ilike(search_term)) | 
            (models.JobOpportunity.company.ilike(search_term))
        )
    
    return query.offset(skip).limit(limit).all()

# ۲. ویرایش یک شغل (PUT)
@router.put("/{job_id}", response_model=schemas.JobOpportunityResponse)
def update_job(job_id: int, job_update: schemas.JobOpportunityUpdate, db: Session = Depends(get_db)):
    db_job = db.query(models.JobOpportunity).filter(models.JobOpportunity.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="شغل مورد نظر یافت نشد")
    
    # به‌روزرسانی فقط فیلدهایی که ارسال شده‌اند
    update_data = job_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
        
    db.commit()
    db.refresh(db_job)
    return db_job

# ۳. حذف یک شغل (DELETE)
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.JobOpportunity).filter(models.JobOpportunity.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="شغل مورد نظر یافت نشد")
    
    db.delete(db_job)
    db.commit()
    return None

# ۴. الگوریتم تطبیق هوشمند ارتقا یافته
@router.get("/match/{user_id}", response_model=List[Dict[str, Any]])
def match_jobs_for_user(
    user_id: int, 
    min_percentage: float = Query(0.0, ge=0.0, le=100.0, description="حداقل درصد تطابق مورد نیاز"),
    market_filter: Optional[schemas.MarketType] = Query(None, description="فیلتر بازار برای پیشنهاد شغل"),
    db: Session = Depends(get_db)
):
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    
    user_skills = set(user.skills)
    if not user_skills:
        return []

    query = db.query(models.JobOpportunity).filter(models.JobOpportunity.status == models.JobStatus.open)
    if market_filter:
        query = query.filter(models.JobOpportunity.market_type == market_filter)
        
    open_jobs = query.all()
    matched_jobs = []
    
    for job in open_jobs:
        job_skills = set(job.required_skills)
        common_skills = user_skills.intersection(job_skills)
        
        if common_skills:
            match_percentage = (len(common_skills) / len(job_skills)) * 100
            
            if match_percentage >= min_percentage:
                matched_jobs.append({
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "market_type": job.market_type.value,
                    "match_percentage": round(match_percentage, 1),
                    "your_matching_skills": list(common_skills),
                    "missing_skills": list(job_skills - user_skills) # ✨ ویژگی جدید: مهارت‌هایی که کم داری
                })
    
    matched_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matched_jobs



@router.post("/webhook/jobs", status_code=status.HTTP_201_CREATED)
def receive_external_jobs(jobs: List[schemas.JobOpportunityCreate], db: Session = Depends(get_db)):

    saved_count = 0
    
    for job_data in jobs:
        # بررسی تکراری نبودن شغل (بر اساس عنوان و شرکت)
        existing_job = db.query(models.JobOpportunity).filter(
            models.JobOpportunity.title == job_data.title,
            models.JobOpportunity.company == job_data.company
        ).first()
        
        if not existing_job:
            new_job = models.JobOpportunity(**job_data.model_dump())
            db.add(new_job)
            saved_count += 1
            
    db.commit()
    
    return {
        "message": f"تعداد {saved_count} شغل جدید با موفقیت ذخیره شد.",
        "total_received": len(jobs)
    }