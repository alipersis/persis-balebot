import os
from flask import Flask, request
from pybale import BaleBot

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", "")

bot = BaleBot(token=BOT_TOKEN)

@bot.on_start
def welcome(chat_id, message):
    bot.send_message(chat_id, "سلام! به ربات پترو پژوهان پرسیس خوش آمدید.")

@bot.on_message
def handle(chat_id, message_text):
    text = message_text.strip()
    if "دوره" in text or "لیست" in text:
        bot.send_message(chat_id, "📚 دوره‌ها:\nPetrel, Geolog, Eclipse, Landmark, Saphir")
    elif "قیمت" in text:
        bot.send_message(chat_id, "💰 قیمت‌ها:\nPetrel:2.2M, Geolog:4.2M, Eclipse:2.1M, Landmark:1.5M, Saphir:1.2M")
    elif "آنلاین" in text:
        bot.send_message(chat_id, "دوره‌های آنلاین ویدئویی هستند. ثبت‌نام: https://petropersis.ir/order")
    elif "آفلاین" in text or "پک" in text:
        bot.send_message(chat_id, "پک آفلاین شامل فلش و مدارک است. ثبت‌نام: https://petropersis.ir/order")
    elif "ثبت" in text:
        bot.send_message(chat_id, "برای ثبت‌نام در سایت وارد شوید:\nhttps://petropersis.ir/order")
        if ADMIN_ID:
            bot.send_message(int(ADMIN_ID), f"📩 کاربر #{chat_id} درخواست ثبت‌نام داد.")
    else:
        bot.send_message(chat_id, "لطفاً بنویسید: دوره، قیمت، آنلاین، آفلاین یا ثبت")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    bot.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    bot.set_webhook(os.getenv("WEBHOOK_URL", ""))
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
