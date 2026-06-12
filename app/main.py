# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app.models import JobSource, UserProfile, JobOpportunity
from app.routes import users, jobs, sources
from app.models import JobSource, UserProfile, JobOpportunity, BlockedIP
from app.middleware import BlockIPMiddleware



# ==================== ساخت اپلیکیشن FastAPI ====================
app = FastAPI(
    title="CareerFlow API",
    description="API هوشمند برای مدیریت و پیشنهاد فرصت‌های شغلی (Market: Local & Global)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ساخت جداول دیتابیس اگر وجود نداشته باشند
Base.metadata.create_all(bind=engine)


# ==================== Middleware CORS ====================
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

app.add_middleware(BlockIPMiddleware)

# ==================== Rate Limiting ====================
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ==================== پنل ادمین با احراز هویت ====================

# سیستم احراز هویت برای پنل ادمین
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        # نام کاربری و رمز عبور ادمین
        if username == "admin" and password == "admin123":
            request.session.update({"admin": username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "admin" in request.session

# ساخت Backend احراز هویت
authentication_backend = AdminAuth(secret_key="your-secret-key-change-this-in-production-12345")


# تعریف ModelView برای سایت‌های کاریابی
class JobSourceAdmin(ModelView, model=JobSource):
    name = "سایت کاریابی"
    name_plural = "سایت‌های کاریابی"
    icon = "fa-solid fa-globe"
    column_list = [
        JobSource.id, 
        JobSource.name, 
        JobSource.display_name, 
        JobSource.is_active, 
        JobSource.is_freelance
    ]
    # فیلدهای Boolean را از فرم حذف می‌کنیم (فقط در لیست نمایش داده می‌شوند)
    form_columns = [
        JobSource.name, 
        JobSource.display_name, 
        JobSource.base_url
    ]
    column_searchable_list = [JobSource.name, JobSource.display_name]
    
    
# تعریف ModelView برای IPهای مسدود شده
class BlockedIPAdmin(ModelView, model=BlockedIP):
    name = "IP مسدود شده"
    name_plural = "IPهای مسدود شده"
    icon = "fa-solid fa-ban"
    column_list = [
        BlockedIP.id,
        BlockedIP.ip_address,
        BlockedIP.reason,
        BlockedIP.blocked_at
    ]
    form_columns = [
        BlockedIP.ip_address,
        BlockedIP.reason
    ]
    column_searchable_list = [BlockedIP.ip_address]


# تعریف ModelView برای کاربران
class UserProfileAdmin(ModelView, model=UserProfile):
    name = "کاربر"
    name_plural = "کاربران"
    icon = "fa-solid fa-user"
    column_list = [
        UserProfile.id, 
        UserProfile.name, 
        UserProfile.email,
        UserProfile.target_market,
        UserProfile.experience_years,
        UserProfile.is_telegram_verified
    ]
    # فیلد Boolean را از فرم حذف می‌کنیم
    form_columns = [
        UserProfile.name,
        UserProfile.target_market,
        UserProfile.experience_years,
        UserProfile.email,
        UserProfile.telegram_chat_id
    ]
    column_searchable_list = [UserProfile.name, UserProfile.email]
    column_details_list = [
        UserProfile.id,
        UserProfile.name,
        UserProfile.skills,
        UserProfile.target_market,
        UserProfile.experience_years,
        UserProfile.email,
        UserProfile.telegram_chat_id,
        UserProfile.telegram_activation_code,
        UserProfile.is_telegram_verified
    ]


# تعریف ModelView برای شغل‌ها
class JobOpportunityAdmin(ModelView, model=JobOpportunity):
    name = "فرصت شغلی"
    name_plural = "فرصت‌های شغلی"
    icon = "fa-solid fa-briefcase"
    column_list = [
        JobOpportunity.id,
        JobOpportunity.title,
        JobOpportunity.company,
        JobOpportunity.market_type,
        JobOpportunity.source,
        JobOpportunity.is_remote,
        JobOpportunity.status
    ]
    # فیلد Boolean را از فرم حذف می‌کنیم
    form_columns = [
        JobOpportunity.title,
        JobOpportunity.company,
        JobOpportunity.market_type,
        JobOpportunity.url,
        JobOpportunity.source,
        JobOpportunity.status
    ]
    column_searchable_list = [JobOpportunity.title, JobOpportunity.company]


# ساخت پنل ادمین با احراز هویت
admin = Admin(
    app, 
    engine, 
    title="CareerFlow Admin Panel",
    authentication_backend=authentication_backend,
    logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
)

# اضافه کردن ModelViewها به پنل
admin.add_view(JobSourceAdmin)
admin.add_view(UserProfileAdmin)
admin.add_view(JobOpportunityAdmin)
admin.add_view(BlockedIPAdmin)


# ==================== Endpointهای اصلی ====================

@app.get("/")
def read_root():
    return {
        "message": "به CareerFlow API خوش آمدید! 🚀",
        "status": "running",
        "database": "connected",
        "admin_panel": "/admin",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CareerFlow Core"}


# ==================== ثبت Routerها ====================
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(sources.router)
