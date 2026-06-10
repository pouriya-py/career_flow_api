# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import users

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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CareerFlow Core"}

app.include_router(users.router)