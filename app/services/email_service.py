# app/services/email_service.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@careerflow.local")


async def send_welcome_email(user_email: str, user_name: str, activation_code: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome to CareerFlow! 🚀"
    msg['From'] = FROM_EMAIL
    msg['To'] = user_email

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; direction: ltr; text-align: left; background-color: #f9fafb; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e5e7eb;">
            <h2 style="color: #7c3aed; margin-top: 0;">Hello {user_name}! 👋</h2>
            <p>Welcome to <strong>CareerFlow</strong> - your AI-powered job matching platform.</p>
            <p>To connect your account to our Telegram bot and receive personalized job recommendations, send this code to the bot:</p>
            <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0; border: 1px dashed #7c3aed;">
                <code style="font-size: 24px; font-weight: bold; color: #7c3aed; letter-spacing: 2px;">{activation_code}</code>
            </div>
            <p style="color: #6b7280; font-size: 14px;">If you didn't request this, please ignore this email.</p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #9ca3af; font-size: 12px;">CareerFlow AI - Smart Job Matching System</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            use_tls=False
        )
        print(f"📧 Welcome email sent to {user_email}")
    except Exception as e:
        print(f"⚠️ Error sending email: {e}")
        print("💡 Make sure Mailpit is running: mailpit")