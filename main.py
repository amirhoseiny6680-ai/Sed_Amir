import os
import requests
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# =========================================================
# ۱. تنظیمات اصلی (حتماً این دو خط را اصلاح کنید)
# =========================================================
TOKEN = "1582396815:AAH7XM585x140aE2iOMVXdHWvaXIGGCXbd8"
CHAT_ID = "413847422"

# تنظیمات لاگ برای عیب‌یابی در رندر
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =========================================================
# ۲. توابع ارسال پیام و گزارش‌دهی
# =========================================================

def send_telegram_msg(text):
    """ارسال متن ساده به تلگرام"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logger.error(f"Error sending message: {response.text}")
        return response.json()
    except Exception as e:
        logger.error(f"Exception in sending message: {e}")
        return None

def job_daily_stock_report():
    """گزارش روزانه ساعت ۱۳:۰۰ - بازار سهام"""
    logger.info("Executing Daily Stock Report (13:00)")
    msg = (
        "📊 *گزارش روزانه بازار سهام (۱۳:۰۰)*\n\n"
        "🔹 وضعیت شاخص کل: [در حال بررسی...]\n"
        "🔹 ورود پول هوشمند: [در حال تحلیل...]\n"
        "🔹 فیلتر حجم مشکوک: [در حال پردازش...]"
    )
    send_telegram_msg(msg)

def job_daily_fund_report():
    """گزارش روزانه ساعت ۱۹:۰۰ - صندوق‌ها"""
    logger.info("Executing Daily Fund Report (19:00)")
    msg = (
        "💰 *گزارش اختصاصی صندوق‌ها (۱۹:۰۰)*\n\n"
        "🔸 صندوق‌های طلا/اهرمی: [در حال بررسی...]\n"
        "🔸 حباب‌سنجی (آتیه مفید): [در حال تحلیل...]\n"
        "🔸 تحلیل مومنتوم صندوق‌ها: [در حال پردازش...]"
    )
    send_telegram_msg(msg)

def job_weekly_special_report():
    """گزارش ویژه هفتگی ساعت ۱۴:۳۰"""
    logger.info("Executing Weekly Special Report (14:30)")
    msg = (
        "🚀 *گزارش جامع هفتگی (۱۴:۳۰)* 🚀\n\n"
        "🔍 *تحلیل ترکیبی Coppock & KST:*\n"
        "✅ فاز ۱ (کف‌سازی): [در حال بررسی...]\n"
        "✅ فاز ۲ (تأیید روند): [در حال بررسی...]\n"
        "✅ فاز ۳ (سوپرگاوی): [در حال بررسی...]\n\n"
        "📈 *وضعیت کلی بازار:* [در حال تحلیل چرخه‌ها...]"
    )
    send_telegram_msg(msg)

# =========================================================
# ۳. مدیریت زمان‌بندی (Scheduler)
# =========================================================

def setup_scheduler():
    scheduler = BackgroundScheduler()
    
    # گزارش روزانه ساعت ۱۳:۰۰ (شنبه تا چهارشنبه)
    scheduler.add_job(job_daily_stock_report, 'cron', day_of_week='mon-fri', hour=13, minute=0)
    
    # گزارش روزانه ساعت ۱۹:۰۰ (شنبه تا چهارشنبه)
    scheduler.add_job(job_daily_fund_report, 'cron', day_of_week='mon-fri', hour=19, minute=0)
    
    # گزارش هفتگی ساعت ۱۴:۳۰ (مثلاً جمعه‌ها - day_of_week='fri')
    # نکته: اگر روز کاری دیگری مد نظر است، 'fri' را به نام روز تغییر دهید
    scheduler.add_job(job_weekly_special_report, 'cron', day_of_week='fri', hour=14, minute=30)
    
    scheduler.start()
    logger.info("Scheduler Started Successfully.")
    return scheduler

# =========================================================
# ۴. وب‌سرور برای زنده نگه داشتن Render
# =========================================================

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Online and Scheduler is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    logger.info(f"Web server running on port {port}")
    server.serve_forever()

# =========================================================
# ۵. نقطه شروع برنامه
# =========================================================

if __name__ == "__main__":
    logger.info("Starting the Bot System...")
       send_telegram_msg("🚀 ربات با موفقیت آنلاین شد و آماده گزارش‌دهی است!")

    # شروع زمان‌بندی در یک Thread جداگانه
    scheduler = setup_scheduler()
    
    # شروع وب‌سرور (باید در Thread اصلی باشد تا برنامه بسته نشود)
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Server error: {e}")
