import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# اطلاعات خودتان را اینجا بگذارید
TOKEN = "8934492635:AAF9ipJHRsukI6hOUrbCjSrIMyXevtNdMY"
CHAT_ID = "413847422"

def send_test_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "✅ ارتباط با رندر برقرار شد!"}
    try:
        response = requests.post(url, json=payload)
        print(f"نتیجه ارسال پیام: {response.text}")
    except Exception as e:
        print(f"خطا در ارسال: {e}")

# اجرای تست در لحظه شروع
send_test_message()

# وب‌سرور برای زنده نگه داشتن رندر
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    server = HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_web_server()
