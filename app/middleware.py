# app/middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import BlockedIP

class BlockIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # دریافت IP کاربر
        client_ip = request.client.host
        
        # بررسی در دیتابیس
        db: Session = SessionLocal()
        try:
            blocked = db.query(BlockedIP).filter(BlockedIP.ip_address == client_ip).first()
            if blocked:
                raise HTTPException(
                    status_code=403,
                    detail=f"دسترسی شما مسدود شده است. دلیل: {blocked.reason or 'نامشخص'}"
                )
        finally:
            db.close()
        
        response = await call_next(request)
        return response