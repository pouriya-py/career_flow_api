# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ۱. ساخت نمونه برنامه FastAPI با متادیتای حرفه‌ای
app = FastAPI(
    title="CareerFlow API",
    description="API هوشمند برای مدیریت و پیشنهاد فرصت‌های شغلی (Market: Local & Global)",
    version="1.0.0",
    docs_url="/docs",  # آدرس مستندات تعاملی (Swagger UI)
    redoc_url="/redoc" # آدرس مستندات جایگزین (ReDoc)
)

# ۲. تنظیمات CORS برای ارتباط امن با فرانت‌اند دوستت
origins = [
    "http://localhost:3000",  # پیش‌فرض Next.js / React
    "http://localhost:5173",  # پیش‌فرض Vite / Vue
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # اجازه تمام متدها (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # اجازه تمام هدرها
)

# ۳. اندپوینت‌های اولیه برای تست سلامت سیستم
@app.get("/")
def read_root():
    return {
        "message": "به CareerFlow API خوش آمدید! 🚀",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CareerFlow Core"}