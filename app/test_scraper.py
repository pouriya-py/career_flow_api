# test_scraper.py
import httpx
import feedparser
from app.database import SessionLocal
from app import models
import asyncio

async def fetch_remotive():
    url = "https://remotive.com/api/remote-jobs?search=python&limit=50"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        return response.json().get('jobs', [])

def fetch_wwr_rss():
    print("  ⏳ در حال خواندن WeWorkRemotely RSS...")
    feed = feedparser.parse("https://weworkremotely.com/categories/remote-programming-jobs.rss")
    jobs = []
    for entry in feed.entries[:20]:
        try:
            jobs.append({
                "title": entry.get('title', 'Unknown Title'),
                "company": entry.get('author', 'WeWorkRemotely'),
                "url": entry.get('link', ''),
                "required_skills": ["Programming", "Remote"],
                "market_type": models.MarketType.GLOBAL,
                "source": "WeWorkRemotely",
                "is_remote": True
            })
        except Exception:
            continue
    return jobs

def fetch_remoteok_rss():
    print("  ⏳ در حال خواندن RemoteOK RSS...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    feed = feedparser.parse("https://remoteok.com/rss", request_headers=headers)
    jobs = []
    for entry in feed.entries[:20]:
        try:
            title = entry.get('title', '').lower()
            summary = entry.get('summary', '').lower()
            
            if "python" in title or "python" in summary:
                jobs.append({
                    "title": entry.get('title', 'Unknown Title'),
                    "company": "RemoteOK",
                    "url": entry.get('link', ''),
                    "required_skills": ["Python", "Remote"],
                    "market_type": models.MarketType.GLOBAL,
                    "source": "RemoteOK",
                    "is_remote": True
                })
        except Exception:
            continue
    return jobs

async def main():
    print("🚀 شروع جمع‌آوری شغل‌ها از منابع متعدد...\n")
    
    remotive_jobs = await fetch_remotive()
    print(f"✅ Remotive API: {len(remotive_jobs)} شغل دریافت شد")
    
    wwr_jobs = fetch_wwr_rss()
    print(f"✅ WeWorkRemotely RSS: {len(wwr_jobs)} شغل دریافت شد")
    
    remoteok_jobs = fetch_remoteok_rss()
    print(f"✅ RemoteOK RSS: {len(remoteok_jobs)} شغل دریافت شد")
    
    all_jobs = []
    for job in remotive_jobs:
        all_jobs.append({
            "title": job.get('title', 'Unknown'),
            "company": job.get('company_name', 'Unknown'),
            "url": job.get('url', ''),
            "required_skills": job.get('tags', [])[:5] or ["Remote"],
            "market_type": models.MarketType.GLOBAL,
            "source": "Remotive",
            "is_remote": True
        })
    all_jobs.extend(wwr_jobs)
    all_jobs.extend(remoteok_jobs)
    
    print(f"\n💾 در حال بررسی و ذخیره {len(all_jobs)} شغل در دیتابیس...")
    
    db = SessionLocal()
    try:
        count = 0
        for job_data in all_jobs:
            if not job_data["url"]:
                continue
                
            existing = db.query(models.JobOpportunity).filter(
                models.JobOpportunity.url == job_data["url"]
            ).first()
            
            if not existing:
                new_job = models.JobOpportunity(**job_data)
                db.add(new_job)
                count += 1
        
        db.commit()
        print(f"🎉 موفق! {count} شغل جدید و یونیک به دیتابیس اضافه شد.")
        print(f"📊 مجموع کل شغل‌های موجود در دیتابیس: {db.query(models.JobOpportunity).count()}")
    except Exception as e:
        print(f"❌ خطا در دیتابیس: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())