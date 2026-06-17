# seed.py
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)

def seed_job_sources(db: Session):
    """Seed active job sources (only verified sources)"""
    sources = [
        models.JobSource(
            name="Remotive",
            display_name="Remotive API",
            base_url="https://remotive.com/api/remote-jobs",
            is_active=True,
            is_freelance=False
        ),
        models.JobSource(
            name="WeWorkRemotely",
            display_name="We Work Remotely",
            base_url="https://weworkremotely.com/categories/remote-programming-jobs.rss",
            is_active=True,
            is_freelance=False
        ),
        models.JobSource(
            name="RemoteOK",
            display_name="RemoteOK",
            base_url="https://remoteok.com/rss",
            is_active=True,
            is_freelance=False
        ),
        models.JobSource(
            name="Python.org",
            display_name="Python.org Jobs",
            base_url="https://www.python.org/jobs/feed/rss/",
            is_active=True,
            is_freelance=False
        ),
        models.JobSource(
            name="HackerNews",
            display_name="Hacker News Who is Hiring",
            base_url="https://hnrss.org/newest?q=who+is+hiring",
            is_active=True,
            is_freelance=False
        ),
    ]
    
    for source in sources:
        existing = db.query(models.JobSource).filter(models.JobSource.name == source.name).first()
        if not existing:
            db.add(source)
    
    db.commit()
    print("✅ Job sources seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_job_sources(db)
    finally:
        db.close()