# app/services/email_service.py
import os
from datetime import datetime

# پوشه‌ای برای ذخیره ایمیل‌های تستی
EMAIL_LOG_DIR = "email_logs"
os.makedirs(EMAIL_LOG_DIR, exist_ok=True)

async def send_welcome_email(user_email: str, user_name: str, activation_code: str):
    """شبیه‌سازی ارسال ایمیل (برای تست)"""
    
    subject = "🎉 به CareerFlow خوش آمدید!"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; direction: rtl;">
        <h2 style="color: #4CAF50;">سلام {user_name} عزیز!</h2>
        
        <p>ثبت‌نام شما در سیستم CareerFlow با موفقیت انجام شد.</p>
        
        <h3>📱 فعال‌سازی تلگرام:</h3>
        <p>برای دریافت اعلان‌های شغلی در تلگرام، لطفاً به ربات ما مراجعه کنید و دستور زیر را بفرستید:</p>
        <code style="background: #f4f4f4; padding: 10px; display: block; margin: 10px 0;">
        /start {activation_code}
        </code>
        
        <h3>🚀 قدم بعدی:</h3>
        <p>سیستم ما به صورت خودکار شغل‌های مناسب شما را پیدا می‌کند و از طریق تلگرام و ایمیل به شما اطلاع می‌دهد.</p>
        
        <hr style="margin: 20px 0;">
        <p style="color: #888; font-size: 12px;">
        این یک ایمیل خودکار از سیستم CareerFlow است.
        </p>
    </body>
    </html>
    """
    
    # ذخیره در فایل HTML برای مشاهده
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{EMAIL_LOG_DIR}/email_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(body)
    
    print(f"📧 ایمیل شبیه‌سازی شده برای {user_email}")
    print(f"📁 فایل ذخیره شده: {filename}")
    
    return {
        "success": True,
        "message": "ایمیل (شبیه‌سازی) با موفقیت ذخیره شد",
        "preview_file": filename
    }