from telegram import Bot
import os

def send_telegram_message(user, text):
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token or not user.telegram_id:
        return
    bot = Bot(token=token)
    bot.send_message(chat_id=user.telegram_id, text=text)
