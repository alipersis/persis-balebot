import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

user_states = {}

def send_message(chat_id, text, button_text=None, button_url=None):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if button_text and button_url:
        data["reply_markup"] = {
            "inline_keyboard": [[
                {"text": button_text, "url": button_url}
            ]]
        }
    requests.post(url, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id or not text:
        return "ignored", 200

    if text == "/start":
        user_states[chat_id] = "main_menu"
        send_message(chat_id,
                     "🎉 خوش آمدید! لطفاً یکی از گزینه‌های زیر را وارد کنید:\n1- دوره‌های آموزشی\n2- کارآموزی\n3- پشتیبانی")
        return "ok", 200

    if user_states.get(chat_id) == "main_menu":
        if text == "1":
            user_states[chat_id] = "course_type"
            send_message(chat_id, "نوع دوره را انتخاب کنید:\n1- آنلاین\n2- آفلاین")
        elif text == "2":
            send_message(chat_id, "برای طی دوره کارآموزی با شرکت تماس بگیرید: ☎️ 02133348963")
        elif text == "3":
            send_message(chat_id, "برای ارتباط با ادمین به آیدی زیر پیام دهید:\n@persisadmin")
        else:
            send_message(chat_id, "لطفاً یکی از گزینه‌های عددی 1 تا 3 را وارد کنید.")
        return "ok", 200

    if user_states.get(chat_id) == "course_type":
        if text == "1":
            user_states[chat_id] = "online_courses"
            send_message(chat_id,
                         "📚 دوره‌های آنلاین:\n1- ژئولاگ\n2- پترل\n3- اکلیپس\n4- لندمارک\n5- سفیر")
        elif text == "2":
            user_states[chat_id] = "offline_courses"
            send_message(chat_id,
                         "📦 دوره‌های آفلاین:\n1- ژئولاگ\n2- پترل\n3- اکلیپس\n4- لندمارک\n5- سفیر\n6- همپسون راسل\n7- لاگ‌های پتروفیزیکی")
        else:
            send_message(chat_id, "لطفاً فقط عدد 1 یا 2 را وارد کنید.")
        return "ok", 200

    if user_states.get(chat_id) == "online_courses":
        user_states[chat_id] = None
        courses = {
            "1": "🎓 دوره جامع آنلاین ژئولاگ – کد 1116\n\n🔸 29 -30 -6 مرداد و شهریور\n🔸 مدرس: سید علی جعفری\n🔸 تصحیحات محیطی، تحلیل تخلخل/تراوایی و تعیین لیتولوژی\n🔸 روش‌های قطعی و احتمالی (Multi‑min)\n🎓 مدرک بین‌ال
