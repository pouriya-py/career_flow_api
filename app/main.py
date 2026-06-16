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
from app.tasks import start_background_tasks

from app.database import engine, Base
from app.models import JobSource, UserProfile, JobOpportunity, BlockedIP
from app.routes import users, jobs, sources


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    print("🚀 Starting background services...")
    await start_background_tasks()
    yield
    # Shutdown tasks
    print("🛑 Shutting down background services...")

app = FastAPI(
    title="CareerFlow API",
    description="Smart API for managing and recommending job opportunities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan 
)

Base.metadata.create_all(bind=engine)


# CORS
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


# Rate Limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# IP Blocking Middleware
from app.middleware import BlockIPMiddleware
app.add_middleware(BlockIPMiddleware)


# Serve static files (for frontend)
import os
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Admin Panel Authentication
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
    column_list = [UserProfile.id, UserProfile.name, UserProfile.email, UserProfile.target_market, UserProfile.experience_years, UserProfile.is_telegram_verified]
    form_columns = [UserProfile.name, UserProfile.target_market, UserProfile.experience_years, UserProfile.email, UserProfile.telegram_chat_id]
    column_searchable_list = [UserProfile.name, UserProfile.email]


class JobOpportunityAdmin(ModelView, model=JobOpportunity):
    name = "Job Opportunity"
    name_plural = "Job Opportunities"
    icon = "fa-solid fa-briefcase"
    column_list = [JobOpportunity.id, JobOpportunity.title, JobOpportunity.company, JobOpportunity.market_type, JobOpportunity.source, JobOpportunity.is_remote, JobOpportunity.status]
    form_columns = [JobOpportunity.title, JobOpportunity.company, JobOpportunity.market_type, JobOpportunity.url, JobOpportunity.source, JobOpportunity.status]
    column_searchable_list = [JobOpportunity.title, JobOpportunity.company]


class BlockedIPAdmin(ModelView, model=BlockedIP):
    name = "Blocked IP"
    name_plural = "Blocked IPs"
    icon = "fa-solid fa-ban"
    column_list = [BlockedIP.id, BlockedIP.ip_address, BlockedIP.reason, BlockedIP.blocked_at]
    form_columns = [BlockedIP.ip_address, BlockedIP.reason]
    column_searchable_list = [BlockedIP.ip_address]


admin = Admin(app, engine, title="CareerFlow Admin", authentication_backend=authentication_backend)
admin.add_view(JobSourceAdmin)
admin.add_view(UserProfileAdmin)
admin.add_view(JobOpportunityAdmin)
admin.add_view(BlockedIPAdmin)


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(sources.router)