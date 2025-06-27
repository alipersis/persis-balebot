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

    # دستور /start
    if text == "/start":
        user_states[chat_id] = "main_menu"
        send_message(chat_id,
                     "🎉 خوش آمدید! لطفاً یکی از گزینه‌های زیر را وارد کنید:\n"
                     "1- دوره‌های آموزشی\n"
                     "2- کارآموزی\n"
                     "3- پشتیبانی")
        return "ok", 200

    # منوی اصلی
    if user_states.get(chat_id) == "main_menu":
        if text == "1":
            user_states[chat_id] = "course_type"
            send_message(chat_id,
                         "نوع دوره را انتخاب کنید:\n"
                         "1- آنلاین\n"
                         "2- آفلاین")
        elif text == "2":
            send_message(chat_id, "برای طی دوره کارآموزی با شرکت تماس بگیرید: ☎️ 02133348963")
        elif text == "3":
            send_message(chat_id, "برای ارتباط با ادمین به آیدی زیر پیام دهید:\n@persisadmin")
        else:
            send_message(chat_id, "لطفاً یکی از گزینه‌های عددی 1 تا 3 را وارد کنید.")
        return "ok", 200

    # انتخاب نوع دوره
    if user_states.get(chat_id) == "course_type":
        if text == "1":
            user_states[chat_id] = "online_courses"
            send_message(chat_id,
                         "📚 دوره‌های آنلاین:\n"
                         "1- ژئولاگ\n"
                         "2- پترل\n"
                         "3- اکلیپس\n"
                         "4- لندمارک\n"
                         "5- سفیر")
        elif text == "2":
            user_states[chat_id] = "offline_courses"
            send_message(chat_id,
                         "📦 دوره‌های آفلاین:\n"
                         "1- ژئولاگ\n"
                         "2- پترل\n"
                         "3- اکلیپس\n"
                         "4- لندمارک\n"
                         "5- سفیر\n"
                         "6- همپسون راسل\n"
                         "7- لاگ‌های پتروفیزیکی")
        else:
            send_message(chat_id, "لطفاً فقط عدد 1 یا 2 را وارد کنید.")
        return "ok", 200

    # دوره‌های آنلاین
    if user_states.get(chat_id) == "online_courses":
        courses = {
            "1": "🎓 دوره جامع آنلاین ژئولاگ – کد 1116\n"
                 "🔸 29-30-6 مرداد و شهریور\n"
                 "🔸 مدرس: سید علی جعفری\n"
                 "🔸 تصحیحات محیطی، تحلیل تخلخل/تراوایی و تعیین لیتولوژی\n"
                 "🔸 روش‌های قطعی و احتمالی (Multi-min)\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: تنها 2,200,000 تومان (دانشجویی)",
            "2": "🎓 دوره جامع آموزش نرم‌افزار Petrel\n"
                 "👨‍🏫 مدرس: سید جواد جعفری\n"
                 "⏱ 11-12-19 مرداد\n"
                 "📚 ورود داده چاه، horizon، مدل‌سازی، OIP و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: ۲۲ میلیون ریال | مدرک: ۲۰ میلیون ریال",
            "3": "🎓 دوره جامع آموزش نرم‌افزار Eclipse\n"
                 "👨‍🏫 مدرس: سید جواد جعفری\n"
                 "⏱ 1-2-25-26 خرداد و تیر\n"
                 "📚 Floviz، Grid، Schedule، RunSpec و ...\n"
                 "🎓 مدرک بین‌المللی (اختیاری)\n"
                 "💰 شهریه: ۲۱ میلیون ریال | مدرک: ۲۰ میلیون ریال",
            "4": "🎓 دوره آموزش Landmark\n"
                 "👨‍🏫 مدرس: سید علی جعفری\n"
                 "⏱ 18-19-26 تیر\n"
                 "📚 طراحی مسیر حفاری، آنالیز هیدرولیک، Wellplan و ...\n"
                 "🎓 مدرک بین‌المللی (اختیاری)\n"
                 "💰 شهریه: 2,050,000 تومان | مدرک: 2,000,000 تومان",
            "5": "🎓 دوره آموزش نرم‌افزار سفیر\n"
                 "👨‍🏫 مدرس: سید جواد جعفری\n"
                 "⏱ 8-9 مرداد\n"
                 "📚 Two Porosity، Gas، Numerical و ...\n"
                 "🎓 مدرک بین‌المللی (اختیاری)\n"
                 "💰 شهریه: 2,100,000 تومان | مدرک: 2,000,000 تومان"
        }
        if text in courses:
            user_states[chat_id] = None
            send_message(chat_id,
                         f"{courses[text]}\n\n"
                         "📥 جهت ثبت‌نام روی دکمه زیر کلیک کنید یا با شماره 02133348963 تماس بگیرید.",
                         button_text="📥 ثبت‌نام در سایت",
                         button_url="https://www.petropersis.ir")
        else:
            send_message(chat_id, "لطفاً عدد مربوط به یکی از دوره‌ها را وارد کنید.")
        return "ok", 200

    # دوره‌های آفلاین
    if user_states.get(chat_id) == "offline_courses":
        courses = {
            "1": "🎓 دوره جامع آفلاین ژئولاگ\n"
                 "🔸 16 ساعت آموزش (4 جلسه)\n"
                 "🔸 مدرس: سید علی جعفری\n"
                 "🔸 تصحیحات محیطی، تحلیل تخلخل/تراوایی و تعیین لیتولوژی\n"
                 "🔸 روش‌های قطعی و احتمالی (Multi-min)\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 4,150,000 تومان (دانشجویی + مدرک)",
            "2": "🎓 دوره آفلاین Petrel\n"
                 "🔸 مدرس: سید جواد جعفری\n"
                 "🔸 ورود داده چاه، horizon، مدل‌سازی، OIP و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 3,950,000 تومان (دانشجویی + مدرک)",
            "3": "🎓 دوره آفلاین Eclipse\n"
                 "🔸 مدرس: سید جواد جعفری\n"
                 "🔸 Floviz، Grid، Schedule، RunSpec و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 4,000,000 تومان (دانشجویی + مدرک)",
            "4": "🎓 دوره آفلاین Landmark\n"
                 "🔸 مدرس: سید علی جعفری\n"
                 "🔸 طراحی مسیر حفاری، آنالیز هیدرولیک، Wellplan و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 3,800,000 تومان (دانشجویی + مدرک)",
            "5": "🎓 دوره آفلاین سفیر\n"
                 "🔸 مدرس: سید جواد جعفری\n"
                 "🔸 Two Porosity، Gas، Numerical و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 3,750,000 تومان (دانشجویی + مدرک)",
            "6": "🎓 دوره آفلاین همپسون راسل\n"
                 "🔸 مدرس: سید علی جعفری\n"
                 "🔸 بررسی لرزه‌ای، معکوس‌سازی، استخراج ویژگی‌ها و ...\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 4,100,000 تومان (دانشجویی + مدرک)",
            "7": "🎓 دوره آفلاین لاگ‌های پتروفیزیکی\n"
                 "🔸 مدرس: سید علی جعفری\n"
                 "🔸 تفسیر NPHI، RHOB، DT، GR و ترکیبی\n"
                 "🎓 مدرک بین‌المللی\n"
                 "💰 شهریه: 3,650,000 تومان (دانشجویی + مدرک)"
        }
        if text in courses:
            user_states[chat_id] = None
            send_message(chat_id,
                         f"{courses[text]}\n\n"
                         "📥 جهت ثبت‌نام روی دکمه زیر کلیک کنید یا با شماره 02133348963 تماس بگیرید.",
                         button_text="📥 ثبت‌نام در سایت",
                         button_url="https://www.petropersis.ir")
        else:
            send_message(chat_id, "لطفاً عدد مربوط به یکی از دوره‌ها را وارد کنید.")
        return "ok", 200

    # اگر هیچ شرطی انجام نشد
    send_message(chat_id, "لطفاً /start را ارسال کنید تا منوی اصلی نمایش داده شود.")
    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True)
