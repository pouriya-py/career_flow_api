# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import users
from app.routes import jobs
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ساخت جداول دیتابیس اگر وجود نداشته باشند (فقط برای محیط توسعه)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerFlow API",
    description="API هوشمند برای مدیریت و پیشنهاد فرصت‌های شغلی (Market: Local & Global)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "به CareerFlow API خوش آمدید! 🚀",
        "status": "running",
        "database": "connected"
    }

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CareerFlow Core"}

app.include_router(users.router)
app.include_router(jobs.router)