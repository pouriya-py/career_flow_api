from sqlalchemy.orm import Session
from app import models
from typing import List


def calculate_match_score(user: models.UserProfile, job: models.JobOpportunity) -> int:
    """محاسبه امتیاز تطابق بین کاربر و شغل (۰ تا ۱۰۰)"""
    score = 0
    
    user_skills = set(skill.lower().strip() for skill in (user.skills or []))
    job_skills = set(skill.lower().strip() for skill in (job.required_skills or []))
    
    if user_skills and job_skills:
        matching_skills = user_skills & job_skills
        if matching_skills:
            skill_score = (len(matching_skills) / max(len(user_skills), 1)) * 70
            score += skill_score
    
    if user.target_market == job.market_type:
        score += 15
    
    if job.is_remote:
        score += 10
    
    if user.experience_years >= 2:
        score += 5
    
    return min(int(score), 100)


def get_matched_jobs(user_id: int, db: Session, limit: int = 20) -> dict:
    """دریافت شغل‌های تطبیق‌یافته برای یک کاربر خاص"""
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        return {"jobs": [], "fallback_used": False, "message": "کاربر یافت نشد"}
    
    all_jobs = db.query(models.JobOpportunity).filter(
        models.JobOpportunity.status == "ACTIVE"
    ).all()
    
    jobs_to_check = all_jobs
    fallback_used = False
    
    if user.favorite_sources:
        favorite_source_names = [source.name for source in user.favorite_sources]
        filtered_jobs = [job for job in all_jobs if job.source in favorite_source_names]
        
        if filtered_jobs:
            jobs_to_check = filtered_jobs
        else:
            jobs_to_check = all_jobs
            fallback_used = True
    
    matched_jobs = []
    for job in jobs_to_check:
        score = calculate_match_score(user, job)
        if score >= 10:
            matched_jobs.append({"job": job, "score": score})
    
    matched_jobs.sort(key=lambda x: x["score"], reverse=True)
    
    if fallback_used:
        message = "شغلی در سایت‌های مورد علاقه شما یافت نشد. پیشنهادات کلی نمایش داده می‌شوند."
    elif not matched_jobs:
        message = "هنوز شغل مناسبی با پروفایل شما پیدا نشد."
    else:
        message = f"{len(matched_jobs)} شغل مناسب پیدا شد"
    
    return {
        "jobs": matched_jobs[:limit],
        "fallback_used": fallback_used,
        "message": message,
        "favorite_sources": [s.name for s in user.favorite_sources] if user.favorite_sources else []
    }