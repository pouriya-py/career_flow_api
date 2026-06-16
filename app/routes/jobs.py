from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from app.services.matching_service import get_matched_jobs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=List[schemas.JobOpportunityResponse])
def get_all_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobOpportunity).offset(skip).limit(limit).all()


@router.post("/webhook/jobs", status_code=status.HTTP_201_CREATED)
def receive_jobs_from_webhook(jobs_data: List[schemas.JobOpportunityCreate], db: Session = Depends(get_db)):
    count = 0
    for job_data in jobs_data:
        existing = db.query(models.JobOpportunity).filter(
            models.JobOpportunity.url == job_data.url
        ).first()
        if not existing:
            new_job = models.JobOpportunity(**job_data.model_dump())
            db.add(new_job)
            count += 1
    
    db.commit()
    return {"message": f"تعداد {count} شغل جدید با موفقیت ذخیره شد"}


@router.get("/matches")
def get_job_matches(
    current_user: models.UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت شغل‌های پیشنهادی هوشمند برای کاربر لاگین شده"""
    result = get_matched_jobs(current_user.id, db, limit=20)
    
    return {
        "user": current_user.name,
        "total_matches": len(result["jobs"]),
        "message": result["message"],
        "fallback_used": result["fallback_used"],
        "favorite_sources": result["favorite_sources"],
        "jobs": [
            {
                "id": item["job"].id,
                "title": item["job"].title,
                "company": item["job"].company,
                "required_skills": item["job"].required_skills,
                "market_type": item["job"].market_type,
                "url": item["job"].url,
                "source": item["job"].source,
                "is_remote": item["job"].is_remote,
                "match_score": item["score"]
            }
            for item in result["jobs"]
        ]
    }