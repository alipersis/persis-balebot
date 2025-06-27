import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# دیکشنری برای ذخیره وضعیت هر کاربر
user_states = {}

def send_message(chat_id, text, button_text=None, button_url=None):
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if button_text and button_url:
        data["reply_markup"] = {
            "inline_keyboard": [
                [{"text": button_text, "url": button_url}]
            ]
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
        courses = {
            "1": """🎓 دوره جامع آنلاین ژئولاگ – کد 1116
🔸 29 -30 -6 مرداد و شهریور
🔸 مدرس: سید علی جعفری
🔸 تصحیحات محیطی، تحلیل تخلخل/تراوایی و تعیین لیتولوژی
🔸 روش‌های قطعی و احتمالی (Multi‑min)
🎓 مدرک بین‌المللی
💰 شهریه: تنها 2,200,000 تومان (دانشجویی)""",
            "2": """🎓 دوره جامع آموزش نرم‌افزار Petrel
👨‍🏫 مدرس: سید جواد جعفری
⏱ 11-12-19 مرداد
📚 ورود داده چاه، horizon، مدل‌سازی، OIP و ...
🎓 مدرک بین‌المللی
💰 شهریه: ۲۲ میلیون ریال | مدرک: ۲۰ میلیون ریال""",
            "3": """🎓 دوره جامع آموزش نرم‌افزار Eclipse
👨‍🏫 مدرس: سید جواد جعفری
⏱ 1-2-25-26 خرداد و تیر
📚 Floviz، Grid، Schedule، RunSpec و ...
🎓 مدرک بین‌المللی (اختیاری)
💰 شهریه: ۲۱ میلیون ریال | مدرک: ۲۰ میلیون ریال""",
            "4": """🎓 دوره آموزش Landmark
👨‍🏫 مدرس: سید علی جعفری
⏱ 18-19-26 تیر
📚 طراحی مسیر حفاری، آنالیز هیدرولیک، Wellplan و ...
🎓 مدرک بین‌المللی (اختیاری)
💰 شهریه: 2.050.000 تومان | مدرک: 2.000.000 تومان""",
            "5": """🎓 دوره آموزش نرم‌افزار سفیر
👨‍🏫 مدرس: سید جواد جعفری
⏱ 8-9 مرداد
📚 Two Porosity، Gas، Numerical و ...
🎓 مدرک بین‌المللی (اختیاری)
💰 شهریه: 2.100.000 تومان | مدرک: 2.000.000 تومان"""
        }
        if text in courses:
            send_message(chat_id,
                         f"{courses[text]}\n\n📥 جهت ثبت‌نام روی دکمه زیر کلیک کنید یا با شماره 02133348963 تماس بگیرید.",
                         button_text="📥 ثبت‌نام در سایت",
                         button_url="https://www.petropersis.ir")
            user_states[chat_id] = None
        else:
            send_message(chat_id, "لطفاً عدد مربوط به دوره را وارد کنید.")
        return "ok", 200

    if user_states.get(chat_id) == "offline_courses":
        courses = {
            "1": """🎓 دوره جامع آفلاین ژئولاگ
🔸 16 ساعت آموزش (4 جلسه)
🔸 مدرس: سید علی جعفری
🔸 تصحیحات محیطی، تحلیل تخلخل/تراوایی و تعیین لیتولوژی
🔸 روش‌های قطعی و احتمالی (Multi‑min)
🎓 مدرک بین‌المللی
💰 شهریه: 4.150.000 تومان (دانشجویی + مدرک)""",
            "2": """🎓 دوره آفلاین Petrel
🔸 مدرس: سید جواد جعفری
🔸 ورود داده چاه، horizon، مدل‌سازی، OIP و ...
🎓 مدرک بین‌المللی
💰 شهریه: 3.950.000 تومان (دانشجویی + مدرک)""",
            "3": """🎓 دوره آفلاین Eclipse
🔸 مدرس: سید جواد جعفری
🔸 Floviz، Grid، Schedule، RunSpec و ...
🎓 مدرک بین‌المللی
💰 شهریه: 4.000.000 تومان (دانشجویی + مدرک)""",
            "4": """🎓 دوره آفلاین Landmark
🔸 مدرس: سید علی جعفری
🔸 طراحی مسیر حفاری، آنالیز هیدرولیک، Wellplan و ...
🎓 مدرک بین‌المللی
💰 شهریه: 3.800.000 تومان (دانشجویی + مدرک)""",
            "5": """🎓 دوره آفلاین سفیر
🔸 مدرس: سید جواد جعفری
🔸 Two Porosity، Gas، Numerical و ...
🎓 مدرک بین‌المللی
💰 شهریه: 3.750.000 تومان (دانشجویی + مدرک)""",
            "6": """🎓 دوره آفلاین همپسون راسل
🔸 مدرس: سید علی جعفری
🔸 بررسی لرزه‌ای، معکوس‌سازی، استخراج ویژگی‌ها و ...
🎓 مدرک بین‌المللی
💰 شهریه: 4.100.000 تومان (دانشجویی + مدرک)""",
            "7": """🎓 دوره آفلاین لاگ‌های پتروفیزیکی
🔸 مدرس: سید علی جعفری
🔸 تفسیر NPHI، RHOB، DT، GR و ترکیبی
🎓 مدرک بین‌المللی
💰 شهریه: 3.650.000 تومان (دانشجویی + مدرک)"""
        }
        if text in courses:
            send_message(chat_id,
                         f"{courses[text]}\n\n📥 جهت ثبت‌نام روی دکمه زیر کلیک کنید یا با شماره 02133348963 تماس بگیرید.",
                         button_text="📥 ثبت‌نام در سایت",
                         button_url="https://www.petropersis.ir")
            user_states[chat_id] = None
        else:
            send_message(chat_id, "لطفاً عدد مربوط به دوره را وارد کنید.")
        return "ok", 200

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
