# app/tasks.py
import os
import asyncio
import httpx
import feedparser
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

from app.database import SessionLocal
from app import models
from app.services.matching_service import get_matched_jobs

load_dotenv()

# --- Bot Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- Telegram Bot Handlers ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Welcome to CareerFlow AI Bot!\n\n"
        "To connect your account, please send your **activation code**.\n"
        "Example: `ACT-A1B2`"
    )

@dp.message(F.text.startswith("ACT-"))
async def handle_activation_code(message: Message):
    code = message.text.strip()
    db = SessionLocal()
    
    try:
        user = db.query(models.UserProfile).filter(
            models.UserProfile.telegram_activation_code == code
        ).first()

        if not user:
            await message.answer("❌ Invalid activation code. Please check and try again.")
            return

        if user.is_telegram_verified:
            await message.answer("⚠️ This account is already verified. You can use /matches command.")
            return

        user.telegram_chat_id = str(message.chat.id)
        user.is_telegram_verified = True
        db.commit()

        await message.answer(
            f"✅ Congratulations {user.name}!\n"
            "Your account has been successfully connected to Telegram.\n\n"
            "You can now use the following command to receive personalized job recommendations:\n"
            "/matches"
        )
    except Exception as e:
        await message.answer("❌ An error occurred. Please try again later.")
        print(f"DB Error: {e}")
    finally:
        db.close()

@dp.message(Command("matches"))
async def cmd_matches(message: Message):
    db = SessionLocal()
    
    try:
        user = db.query(models.UserProfile).filter(
            models.UserProfile.telegram_chat_id == str(message.chat.id)
        ).first()

        if not user or not user.is_telegram_verified:
            await message.answer("⚠️ Your account is not verified. Please send your activation code first (ACT-...).")
            return

        result = get_matched_jobs(user.id, db, limit=3)
        matched_jobs = result["jobs"]

        if not matched_jobs:
            await message.answer(
                "😔 No suitable jobs found for your profile at the moment.\n"
                "Please update your skills in the dashboard or check back later."
            )
            return

        await message.answer(f"🎯 Found {len(matched_jobs)} top matches for you:\n")

        for item in matched_jobs:
            job = item["job"]
            score = item["score"]
            
            text = (
                f"💼 *{job.title}*\n"
                f"🏢 {job.company}\n"
                f"🔗 Source: {job.source}\n"
                f"🎯 Match Score: *{score}%*\n"
                f"🔗 [View Job]({job.url})"
            )
            await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer("❌ Error fetching job recommendations.")
        print(f"Match Error: {e}")
    finally:
        db.close()

# --- Scraper Functions ---
async def fetch_remotive():
    """Fetch jobs from Remotive API"""
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://remotive.com/api/remote-jobs?search=python&limit=30", timeout=30.0)
            data = res.json()
            jobs = []
            for job in data.get('jobs', []):
                jobs.append({
                    "title": job.get('title', 'Unknown'),
                    "company": job.get('company_name', 'Unknown'),
                    "url": job.get('url', ''),
                    "required_skills": job.get('tags', [])[:5] or ["Remote"],
                    "market_type": models.MarketType.GLOBAL,
                    "source": "Remotive",
                    "is_remote": True
                })
            return jobs
    except Exception as e:
        print(f"❌ Error fetching Remotive: {e}")
        return []

def fetch_weworkremotely():
    """Fetch jobs from WeWorkRemotely RSS"""
    try:
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
    except Exception as e:
        print(f"❌ Error fetching WeWorkRemotely: {e}")
        return []

def fetch_remoteok():
    """Fetch jobs from RemoteOK RSS"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        feed = feedparser.parse("https://remoteok.com/rss", request_headers=headers)
        jobs = []
        for entry in feed.entries[:20]:
            try:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if "python" in title or "python" in summary or "developer" in title:
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
    except Exception as e:
        print(f"❌ Error fetching RemoteOK: {e}")
        return []

def fetch_python_org():
    """Fetch jobs from Python.org Jobs RSS"""
    try:
        feed = feedparser.parse("https://www.python.org/jobs/feed/rss/")
        jobs = []
        for entry in feed.entries[:15]:
            try:
                jobs.append({
                    "title": entry.get('title', 'Unknown Title'),
                    "company": entry.get('author', 'Python.org'),
                    "url": entry.get('link', ''),
                    "required_skills": ["Python"],
                    "market_type": models.MarketType.GLOBAL,
                    "source": "Python.org",
                    "is_remote": False
                })
            except Exception:
                continue
        return jobs
    except Exception as e:
        print(f"❌ Error fetching Python.org: {e}")
        return []

def fetch_hackernews():
    """Fetch jobs from Hacker News Who is Hiring"""
    try:
        feed = feedparser.parse("https://hnrss.org/newest?q=who+is+hiring")
        jobs = []
        for entry in feed.entries[:15]:
            try:
                title = entry.get('title', '')
                if "python" in title.lower() or "developer" in title.lower():
                    jobs.append({
                        "title": title,
                        "company": "Hacker News",
                        "url": entry.get('link', ''),
                        "required_skills": ["Python", "Developer"],
                        "market_type": models.MarketType.GLOBAL,
                        "source": "HackerNews",
                        "is_remote": False
                    })
            except Exception:
                continue
        return jobs
    except Exception as e:
        print(f"❌ Error fetching HackerNews: {e}")
        return []

# --- Automated Scraper Task ---
async def run_automated_scraper():
    print("\n" + "="*60)
    print("⏰ [Scheduler] Starting automated job scraping...")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Fetch from all sources concurrently
        remotive_jobs = await fetch_remotive()
        print(f"✅ Remotive: {len(remotive_jobs)} jobs")
        
        wwr_jobs = fetch_weworkremotely()
        print(f"✅ WeWorkRemotely: {len(wwr_jobs)} jobs")
        
        remoteok_jobs = fetch_remoteok()
        print(f"✅ RemoteOK: {len(remoteok_jobs)} jobs")
        
        python_org_jobs = fetch_python_org()
        print(f"✅ Python.org: {len(python_org_jobs)} jobs")
        
        hn_jobs = fetch_hackernews()
        print(f"✅ HackerNews: {len(hn_jobs)} jobs")
        
        # Aggregate all jobs
        all_jobs = []
        all_jobs.extend(remotive_jobs)
        all_jobs.extend(wwr_jobs)
        all_jobs.extend(remoteok_jobs)
        all_jobs.extend(python_org_jobs)
        all_jobs.extend(hn_jobs)
        
        print(f"\n📊 Total jobs fetched: {len(all_jobs)}")
        
        # Save to database (prevent duplicates)
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
        print(f"\n🎉 Success! {count} new jobs added to database.")
        print(f"📊 Total jobs in database: {db.query(models.JobOpportunity).count()}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ [Scheduler] Error in scraping: {e}")
        db.rollback()
    finally:
        db.close()

# --- Auto-send Jobs to Users ---
async def send_daily_jobs_to_users():
    """Send top jobs to all verified users"""
    print("\n" + "="*60)
    print("📬 [Scheduler] Starting automated job delivery to users...")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Get all verified users
        users = db.query(models.UserProfile).filter(
            models.UserProfile.is_telegram_verified == True,
            models.UserProfile.telegram_chat_id != None
        ).all()
        
        print(f"👥 Verified users: {len(users)}")
        
        sent_count = 0
        for user in users:
            try:
                # Get top 3 jobs for this user
                result = get_matched_jobs(user.id, db, limit=3)
                matched_jobs = result["jobs"]
                
                if not matched_jobs:
                    continue
                
                # Send message to user
                await bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=f"🌅 Good morning {user.name}!\n\n"
                         f"🎯 Found {len(matched_jobs)} top job matches for you:"
                )
                
                for item in matched_jobs:
                    job = item["job"]
                    score = item["score"]
                    
                    text = (
                        f"💼 *{job.title}*\n"
                        f"🏢 {job.company}\n"
                        f"🔗 Source: {job.source}\n"
                        f"🎯 Match Score: *{score}%*\n"
                        f"🔗 [View Job]({job.url})"
                    )
                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=text,
                        parse_mode="Markdown"
                    )
                
                sent_count += 1
                print(f"✅ Jobs sent to {user.name}")
                
                # Prevent Telegram rate limit
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Error sending to {user.name}: {e}")
                continue
        
        print(f"\n🎉 Auto-delivery completed! {sent_count} users received jobs.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error in auto-delivery: {e}")
    finally:
        db.close()

# --- Start Background Tasks ---
async def start_background_tasks():
    if BOT_TOKEN:
        asyncio.create_task(dp.start_polling(bot))
        print("✅ Telegram bot started in background.")
    else:
        print("⚠️ BOT_TOKEN not set in .env. Telegram bot will not run.")

    # Schedule scraper: every 30 minutes
    scheduler.add_job(run_automated_scraper, 'interval', minutes=30)
    
    # Schedule auto-delivery: every day at 9 AM
    scheduler.add_job(send_daily_jobs_to_users, 'cron', hour=9, minute=0)
    print("✅ Scheduled auto job delivery (daily at 9 AM).")
    
    scheduler.start()
    print("✅ Scheduled scraper (every 30 minutes).")
    
    # Run scraper immediately on startup
    await run_automated_scraper()