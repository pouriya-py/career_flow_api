# seed.py
from app.database import engine, Base, SessionLocal
from app import models

# ساخت جداول دیتابیس اگر وجود نداشته باشند
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # ۱. لیست سایت‌های کاریابی و فریلنسری
    sources_data = [
        {"name": "Jobinja", "display_name": "جابینجا", "base_url": "https://jobinja.ir", "is_active": True, "is_freelance": False},
        {"name": "LinkedIn", "display_name": "لینکدین", "base_url": "https://linkedin.com/jobs", "is_active": True, "is_freelance": False},
        {"name": "Indeed", "display_name": "ایندید", "base_url": "https://indeed.com", "is_active": True, "is_freelance": False},
        {"name": "WeWorkRemotely", "display_name": "We Work Remotely", "base_url": "https://weworkremotely.com", "is_active": True, "is_freelance": False},
        {"name": "Quera", "display_name": "کوئرا", "base_url": "https://quera.ir", "is_active": True, "is_freelance": False},
        {"name": "Upwork", "display_name": "آپورک", "base_url": "https://upwork.com", "is_active": True, "is_freelance": True},
        {"name": "Freelancer", "display_name": "فریلنسر", "base_url": "https://freelancer.com", "is_active": True, "is_freelance": True},
        {"name": "Ponisha", "display_name": "پونیشا", "base_url": "https://ponisha.ir", "is_active": True, "is_freelance": True},
    ]

    # ۲. لیست شغل‌های نمونه
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "Digikala",
            "required_skills": ["Python", "Django", "PostgreSQL", "Docker"],
            "market_type": models.MarketType.IRAN,  # 👈 اصلاح شد
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": False
        },
        {
            "title": "Remote FastAPI Engineer",
            "company": "TechGlobal Inc.",
            "required_skills": ["Python", "FastAPI", "AWS", "Redis"],
            "market_type": models.MarketType.GLOBAL,  # 👈 اصلاح شد
            "url": "https://linkedin.com/jobs/...",
            "source": "LinkedIn",
            "is_remote": True
        },
        {
            "title": "Frontend Developer (React)",
            "company": "Snapp",
            "required_skills": ["React", "TypeScript", "TailwindCSS"],
            "market_type": models.MarketType.IRAN,  # 👈 اصلاح شد
            "url": "https://jobinja.ir/...",
            "source": "Jobinja",
            "is_remote": True
        },
        {
            "title": "DevOps Engineer",
            "company": "Canonical",
            "required_skills": ["Linux", "Kubernetes", "Python", "CI/CD"],
            "market_type": models.MarketType.GLOBAL,  # 👈 اصلاح شد
            "url": "https://weworkremotely.com/...",
            "source": "WeWorkRemotely",
            "is_remote": True
        }
    ]
    
    # پاک کردن داده‌های قبلی برای شروع پاک
    db.query(models.JobOpportunity).delete()
    db.query(models.UserProfile).delete()
    db.query(models.JobSource).delete()
    db.commit()
    
    # اضافه کردن سایت‌ها به دیتابیس
    for source_data in sources_data:
        new_source = models.JobSource(**source_data)
        db.add(new_source)
        
    # اضافه کردن شغل‌ها به دیتابیس
    for job_data in jobs_data:
        new_job = models.JobOpportunity(**job_data)
        db.add(new_job)
        
    # اضافه کردن یک کاربر تستی
    test_user = models.UserProfile(
        name="Pouriya Test",
        skills=["Python", "FastAPI", "Docker", "Git"],
        target_market=models.MarketType.GLOBAL,  # 👈 اصلاح شد
        experience_years=3,
        email="pouriya@example.com"
    )
    db.add(test_user)
    
    db.commit()
    print("✅ دیتابیس با موفقیت با داده‌های نمونه پر شد!")
    db.close()

if __name__ == "__main__":
    seed_database()