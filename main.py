import requests
import os
import schedule
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# ==========================================
# تنظیمات اصلی (اینجا را با اطلاعات خود پر کنید)
# ==========================================
TOKEN = "1582396815:AAH7XM585x140aE2iOMVXdHWvaXIGGCXbd8"
CHAT_ID = "413847422"

# ==========================================
# توابع کمکی و ارسال گزارش
# ==========================================

def send_telegram_message(message):
    """ارسال پیام به تلگرام"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[{datetime.now()}] پیام با موفقیت ارسال شد.")
        else:
            print(f"[{datetime.now()}] خطا در 
