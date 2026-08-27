import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import schedule

# ==================== تنظیمات ربات ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8934492635:AAF9ipJHRsukI6hOUrbCjSrIMyXevtNdMY")
CHAT_ID = os.environ.get("CHAT_ID", "413847422")

# ==================== تابع ارسال پیام به تلگرام ====================
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        print(f"Telegram response: {res.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

# ==================== گزارش‌های زمان‌بندی شده ====================
def report_stock_13():
    msg = """📊 **گزارش بازار سهام و ورود پول هوشمند (ساعت ۱۳:۰۰)**
• شاخص کل و هم‌وزن در وضعیت تعادلی
• فیلتر ورود پول هوشمند: نمادهای مستعد با سرانه خرید بالا شناسایی شدند.
• سیگنال هفتگی Coppock/KST: بررسی فازهای کف‌سازی و ورود نقدینگی."""
    send_telegram_message(msg)

def report_funds_19():
    msg = """💎 **گزارش اختصاصی صندوق‌ها و حباب‌سنجی (ساعت ۱۹:۰۰)**
• صندوق‌های طلا (عیار، کهربا) و اهرمی
• وضعیت صندوق آتیه مفید (IRTKMOFD0001)
• سیگنال‌های فاز ۳ سوپرگاوی و مومنتوم هفتگی."""
    send_telegram_message(msg)

# زمان‌بندی‌ها (شنبه تا چهارشنبه)
schedule.every().day.at("09:30").do(report_stock_13)  # معادل ساعت ۱۳:۰۰ ایران (به وقت سرور گرینویچ UTC)
schedule.every().day.at("15:30").do(report_funds_19)  # معادل ساعت ۱۹:۰۰ ایران

def run_scheduler():
    print("Scheduler started...")
    # یک پیام تست در بدو روشن شدن ارسال می‌شود
    send_telegram_message("🟢 ربات رصد بازار با موفقیت روی سرور رندر فعال شد!")
    while True:
        schedule.run_pending()
        time.sleep(30)

# ==================== وب‌سرور برای زنده نگه داشتن Render ====================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Web server listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # اجرای زمان‌بند در پس‌زمینه
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    
    # اجرای وب‌سرور در ترد اصلی برای رندر
    run_web_server()
