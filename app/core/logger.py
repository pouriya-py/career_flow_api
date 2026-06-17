# app/core/logger.py
import sys
from loguru import logger

# حذف تنظیمات پیش‌فرض
logger.remove()

# افزودن لاگ به کنسول (با رنگ و فرمت زیبا)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# افزودن لاگ به فایل (برای بررسی خطاها در سرور)
logger.add(
    "logs/app.log",
    rotation="10 MB",  # اگر فایل به ۱۰ مگابایت رسید، فایل جدید می‌سازد
    retention="7 days", # لاگ‌های قدیمی‌تر از ۷ روز را پاک می‌کند
    level="DEBUG",
    encoding="utf-8"
)

# ساخت پوشه logs اگر وجود نداشته باشد
import os
os.makedirs("logs", exist_ok=True)