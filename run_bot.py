# run_bot.py
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

from app.database import SessionLocal
from app import models
from app.services.matching_service import get_matched_jobs

# بارگذاری متغیرهای محیطی
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("لطفاً توکن ربات را در فایل .env قرار دهید.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 سلام! به ربات هوشمند CareerFlow خوش آمدید.\n\n"
        "برای اتصال حساب کاربری خود، لطفاً **کد فعال‌سازی** که هنگام ثبت‌نام در سایت دریافت کردید را ارسال کنید.\n"
        "مثال: `ACT-A1B2`"
    )


@dp.message(F.text.startswith("ACT-"))
async def handle_activation_code(message: Message):
    code = message.text.strip()
    db = SessionLocal()
    
    try:
        user = db.query(models.UserProfile).filter(
            models.UserProfile.telegram_activation_code == code
        ).first()

        if not user:
            await message.answer("❌ کد فعال‌سازی نامعتبر است. لطفاً دوباره بررسی کنید.")
            return

        if user.is_telegram_verified:
            await message.answer("⚠️ این حساب قبلاً فعال شده است. می‌توانید از دستور /matches استفاده کنید.")
            return

        # فعال‌سازی کاربر
        user.telegram_chat_id = str(message.chat.id)
        user.is_telegram_verified = True
        db.commit()

        await message.answer(
            f"✅ تبریک {user.name} عزیز!\n"
            "حساب شما با موفقیت به تلگرام متصل شد.\n\n"
            "حالا می‌توانید از دستور زیر برای دریافت شغل‌های پیشنهادی استفاده کنید:\n"
            "/matches"
        )
    except Exception as e:
        await message.answer("❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
        print(f"DB Error: {e}")
    finally:
        db.close()


@dp.message(Command("matches"))
async def cmd_matches(message: Message):
    db = SessionLocal()
    
    try:
        user = db.query(models.UserProfile).filter(
            models.UserProfile.telegram_chat_id == str(message.chat.id)
        ).first()

        if not user or not user.is_telegram_verified:
            await message.answer("⚠️ حساب شما تأیید نشده است. لطفاً ابتدا کد فعال‌سازی (ACT-...) را ارسال کنید.")
            return

        result = get_matched_jobs(user.id, db, limit=3)
        matched_jobs = result["jobs"]

        if not matched_jobs:
            await message.answer(
                "😔 فعلاً شغل مناسبی با پروفایل شما پیدا نشد.\n"
                "لطفاً مهارت‌های خود را در سایت به‌روزرسانی کنید."
            )
            return

        await message.answer(f"🎯 {len(matched_jobs)} شغل برتر برای شما پیدا شد:\n")

        for item in matched_jobs:
            job = item["job"]
            score = item["score"]
            
            text = (
                f"💼 *{job.title}*\n"
                f"🏢 {job.company}\n"
                f"🔗 منبع: {job.source}\n"
                f"🎯 امتیاز تطابق: *{score}%*\n"
                f"🔗 [مشاهده آگهی]({job.url})"
            )
            await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer("❌ خطایی در دریافت شغل‌ها رخ داد.")
        print(f"Match Error: {e}")
    finally:
        db.close()


async def main():
    print("🤖 ربات CareerFlow در حال اجرا است... (برای توقف Ctrl+C را بزنید)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())