import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id or not text:
        return "ignored", 200

    if "سلام" in text or "/start" in text:
        send_message(chat_id, "سلام! خوش آمدید به ربات پترو پژوهان پرسیس.")
    elif "دوره" in text:
        send_message(chat_id, "📚 دوره‌ها:\nPetrel, Geolog, Eclipse, Landmark, Saphir")
    elif "قیمت" in text:
        send_message(chat_id, "💰 قیمت‌ها:\nPetrel: 2.2M\nGeolog: 4.2M\nEclipse: 2.1M\nLandmark: 1.5M\nSaphir: 1.2M")
    elif "ثبت" in text:
        send_message(chat_id, "برای ثبت‌نام وارد سایت شوید:\nhttps://petropersis.ir/order")
        if ADMIN_ID:
            send_message(ADMIN_ID, f"📥 کاربر {chat_id} درخواست ثبت‌نام داد.")
    else:
        send_message(chat_id, "دستور را متوجه نشدم. لطفاً بپرسید: دوره، قیمت، ثبت‌نام...")

    return "ok", 200

if __name__ == "__main__":
    # تنظیم webhook فقط یک‌بار، نه در اجرای عادی
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        requests.post(f"{API_URL}/setWebhook", json={"url": webhook_url})
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
