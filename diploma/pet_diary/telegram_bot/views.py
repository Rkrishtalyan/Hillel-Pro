import os
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils.encoding import force_str

from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from accounts.models import CustomUser

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
dp = application.dispatcher

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Используй /link <email>, чтобы связать аккаунт."
    )

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи /link <email>")
        return
    email = context.args[0]
    try:
        user = CustomUser.objects.get(email=email)
        user.telegram_id = update.effective_user.id
        user.save()
        await update.message.reply_text(f"Успешно связал Телеграм с {email}!")
    except CustomUser.DoesNotExist:
        await update.message.reply_text("Пользователь с таким email не найден.")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я бот. Используй /start или /link <email>.")

dp.add_handler(CommandHandler("start", start_command))
dp.add_handler(CommandHandler("link", link_command))
dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = force_str(request.body)
        update = Update.de_json(data, bot)
        dp.process_update(update)
        return JsonResponse({"ok": True})
    else:
        return HttpResponseNotAllowed(["POST"])
