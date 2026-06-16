# test_sources.py
import httpx
import feedparser
import asyncio

async def test_source(name, url, is_rss=True):
    """تست یک منبع شغلی"""
    print(f"\n{'='*60}")
    print(f"🔍 تست {name}: {url}")
    print(f"{'='*60}")
    
    try:
        if is_rss:
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                print(f"❌ خطا: {feed.bozo_exception}")
                return False
            
            print(f"✅ موفق! تعداد ورودی‌ها: {len(feed.entries)}")
            if feed.entries:
                first = feed.entries[0]
                print(f"   عنوان: {first.get('title', 'N/A')}")
                print(f"   لینک: {first.get('link', 'N/A')}")
            return True
        else:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, timeout=30.0)
                if res.status_code == 200:
                    data = res.json()
                    jobs = data.get('jobs', [])
                    print(f"✅ موفق! تعداد شغل‌ها: {len(jobs)}")
                    if jobs:
                        print(f"   عنوان: {jobs[0].get('title', 'N/A')}")
                    return True
                else:
                    print(f"❌ خطای HTTP: {res.status_code}")
                    return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

async def main():
    sources = [
        # سایت‌های بین‌المللی
        ("Remotive API", "https://remotive.com/api/remote-jobs?search=python&limit=5", False),
        ("WeWorkRemotely RSS", "https://weworkremotely.com/categories/remote-programming-jobs.rss", True),
        ("RemoteOK RSS", "https://remoteok.com/rss", True),
        ("Python.org Jobs", "https://www.python.org/jobs/feed/rss/", True),
        ("Real Python Jobs", "https://realpython.com/jobs/feed/rss/", True),
        ("Hacker News Who is Hiring", "https://hnrss.org/newest?q=who+is+hiring", True),
        ("Stack Overflow Jobs", "https://stackoverflow.com/jobs/feed?l=remote&md=python", True),
        
        # سایت‌های ایرانی (احتمالاً کار نمی‌کنند)
        ("Jobinja RSS (تست)", "https://jobinja.ir/rss", True),
        ("Quera RSS (تست)", "https://quera.ir/rss", True),
    ]
    
    results = []
    for name, url, is_rss in sources:
        success = await test_source(name, url, is_rss)
        results.append((name, success))
    
    print(f"\n\n{'='*60}")
    print("📊 خلاصه نتایج:")
    print(f"{'='*60}")
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")

if __name__ == "__main__":
    asyncio.run(main())