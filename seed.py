# seed.py
from app.database import engine, Base, SessionLocal
from app import models

# ساخت جداول (اگر قبلاً career_flow.db را حذف کرده باشی، این جداول جدید را می‌سازد)
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # لیست شغل‌های نمونه (ترکیبی از ایران، جهان، دورکاری و منابع مختلف)
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "Digikala",
            "required_skills": ["Python", "Django", "PostgreSQL", "Docker"],
            "market_type": models.MarketType.iran,
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": False
        },
        {
            "title": "Remote FastAPI Engineer",
            "company": "TechGlobal Inc.",
            "required_skills": ["Python", "FastAPI", "AWS", "Redis"],
            "market_type": models.MarketType.global_market,
            "url": "https://linkedin.com/jobs/...",
            "source": "LinkedIn",
            "is_remote": True
        },
        {
            "title": "Frontend Developer (React)",
            "company": "Snapp",
            "required_skills": ["React", "TypeScript", "TailwindCSS"],
            "market_type": models.MarketType.iran,
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": True
        },
        {
            "title": "DevOps Engineer",
            "company": "Canonical",
            "required_skills": ["Linux", "Kubernetes", "Python", "CI/CD"],
            "market_type": models.MarketType.global_market,
            "url": "https://weworkremotely.com/...",
            "source": "WeWorkRemotely",
            "is_remote": True
        },
        {
            "title": "Junior Backend Developer",
            "company": "Cafe Bazaar",
            "required_skills": ["Python", "FastAPI", "Git"],
            "market_type": models.MarketType.iran,
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": False
        },
        {
            "title": "Full Stack Developer (Node.js)",
            "company": "StartupXYZ",
            "required_skills": ["Node.js", "React", "MongoDB", "Docker"],
            "market_type": models.MarketType.global_market,
            "url": "https://indeed.com/...",
            "source": "Indeed",
            "is_remote": True
        },
        {
            "title": "Data Scientist",
            "company": "AliExpress",
            "required_skills": ["Python", "Pandas", "Machine Learning", "SQL"],
            "market_type": models.MarketType.global_market,
            "url": "https://linkedin.com/jobs/...",
            "source": "LinkedIn",
            "is_remote": True
        },
        {
            "title": "Mobile Developer (Flutter)",
            "company": "Tapsi",
            "required_skills": ["Flutter", "Dart", "REST API"],
            "market_type": models.MarketType.iran,
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": False
        }
    ]
    
    # پاک کردن داده‌های قبلی (اختیاری، برای شروع پاک)
    db.query(models.JobOpportunity).delete()
    db.query(models.UserProfile).delete()
    db.commit()
    
    # اضافه کردن شغل‌ها به دیتابیس
    for job_data in jobs_data:
        new_job = models.JobOpportunity(**job_data)
        db.add(new_job)
        
    # اضافه کردن یک کاربر تستی برای تطبیق
    test_user = models.UserProfile(
        name="Pouriya Test",
        skills=["Python", "FastAPI", "Docker", "Git"],
        target_market=models.MarketType.global_market,
        experience_years=3
    )
    db.add(test_user)
    
    db.commit()
    print("✅ دیتابیس با موفقیت با داده‌های نمونه پر شد!")
    db.close()

if __name__ == "__main__":
    seed_database()