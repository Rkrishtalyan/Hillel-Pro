import os
from telegram import Bot

_telegram_bot = None

def _bot_send_message(bot: Bot, chat_id: int, text: str):
    bot.send_message(chat_id=chat_id, text=text)

def send_telegram_message(user, text):
    if not user.telegram_id:
        return

    global _telegram_bot
    if not _telegram_bot:
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            return
        _telegram_bot = Bot(token=token)

    _bot_send_message(_telegram_bot, user.telegram_id, text)
