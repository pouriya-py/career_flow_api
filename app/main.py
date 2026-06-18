from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import os

from app.database import engine, Base
from app.models import JobSource, UserProfile, JobOpportunity, BlockedIP
from app.routes import users, jobs, sources
from app.tasks import start_background_tasks
from app.middleware import BlockIPMiddleware


# --- Lifespan (Startup & Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting background services...")
    await start_background_tasks()
    yield
    # Shutdown
    print("🛑 Shutting down background services...")


# --- FastAPI App ---
app = FastAPI(
    title="CareerFlow API",
    description="Smart API for managing and recommending job opportunities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

Base.metadata.create_all(bind=engine)


# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- IP Blocking Middleware ---
app.add_middleware(BlockIPMiddleware)


# --- Static Files ---
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Admin Panel Authentication ---
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == "admin" and password == "admin123":
            request.session.update({"admin": username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "admin" in request.session


authentication_backend = AdminAuth(secret_key="career-flow-secret-key-2026-change-in-production")


# --- Admin Panel Views ---
class JobSourceAdmin(ModelView, model=JobSource):
    name = "Job Source"
    name_plural = "Job Sources"
    icon = "fa-solid fa-globe"
    column_list = [JobSource.id, JobSource.name, JobSource.display_name, JobSource.is_active, JobSource.is_freelance]
    form_columns = [JobSource.name, JobSource.display_name, JobSource.base_url]
    column_searchable_list = [JobSource.name, JobSource.display_name]


class UserProfileAdmin(ModelView, model=UserProfile):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [
        UserProfile.id, 
        UserProfile.name, 
        UserProfile.email, 
        UserProfile.target_market, 
        UserProfile.experience_years, 
        UserProfile.is_telegram_verified
    ]
    form_columns = [
        UserProfile.name, 
        UserProfile.target_market, 
        UserProfile.experience_years, 
        UserProfile.email, 
        UserProfile.telegram_chat_id
    ]
    column_searchable_list = [UserProfile.name, UserProfile.email]


class JobOpportunityAdmin(ModelView, model=JobOpportunity):
    name = "Job Opportunity"
    name_plural = "Job Opportunities"
    icon = "fa-solid fa-briefcase"
    column_list = [
        JobOpportunity.id, 
        JobOpportunity.title, 
        JobOpportunity.company, 
        JobOpportunity.source, 
        JobOpportunity.is_remote, 
        JobOpportunity.status
    ]
    form_columns = [
        JobOpportunity.title, 
        JobOpportunity.company, 
        JobOpportunity.url, 
        JobOpportunity.source, 
        JobOpportunity.status
    ]
    column_searchable_list = [JobOpportunity.title, JobOpportunity.company]
    column_default_sort = ("id", True)


class BlockedIPAdmin(ModelView, model=BlockedIP):
    name = "Blocked IP"
    name_plural = "Blocked IPs"
    icon = "fa-solid fa-ban"
    column_list = [BlockedIP.id, BlockedIP.ip_address, BlockedIP.reason, BlockedIP.blocked_at]
    form_columns = [BlockedIP.ip_address, BlockedIP.reason]
    column_searchable_list = [BlockedIP.ip_address]


# --- Initialize Admin Panel ---
admin = Admin(
    app, 
    engine, 
    title="CareerFlow Admin", 
    authentication_backend=authentication_backend
)
admin.add_view(JobSourceAdmin)
admin.add_view(UserProfileAdmin)
admin.add_view(JobOpportunityAdmin)
admin.add_view(BlockedIPAdmin)


# --- Root Endpoint (Frontend) ---
@app.get("/")
def read_root():
    return FileResponse("static/index.html")


# --- Health Check ---
@app.head("/")
def head_root():
    """Health check for Render"""
    from fastapi.responses import Response
    return Response(status_code=200)


# --- Admin Stats API (JSON) ---
@app.get("/api/stats")
def admin_stats():
    """Admin dashboard statistics - JSON API"""
    from app.database import SessionLocal
    from sqlalchemy import func
    
    db = SessionLocal()
    try:
        total_users = db.query(UserProfile).count()
        verified_users = db.query(UserProfile).filter(UserProfile.is_telegram_verified == True).count()
        total_jobs = db.query(JobOpportunity).count()
        active_jobs = db.query(JobOpportunity).filter(JobOpportunity.status == "ACTIVE").count()
        remote_jobs = db.query(JobOpportunity).filter(JobOpportunity.is_remote == True).count()
        total_sources = db.query(JobSource).filter(JobSource.is_active == True).count()
        
        jobs_by_source_query = db.query(
            JobOpportunity.source, 
            func.count(JobOpportunity.id).label('count')
        ).group_by(JobOpportunity.source).all()
        
        jobs_by_source = {source or 'Unknown': count for source, count in jobs_by_source_query}
        
        return {
            "total_users": total_users,
            "verified_users": verified_users,
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "remote_jobs": remote_jobs,
            "total_sources": total_sources,
            "jobs_by_source": jobs_by_source
        }
    finally:
        db.close()


# --- Include Routers ---
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(sources.router)
