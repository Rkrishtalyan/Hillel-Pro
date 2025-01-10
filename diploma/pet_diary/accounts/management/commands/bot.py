import os
import logging
import asyncio

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from accounts.models import CustomUser

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = "Run Telegram bot in long-polling mode"

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Используй /link <email>, чтобы связать аккаунт."
        )

    async def link_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Укажи /link <email>")
            return
        email = context.args[0]
        try:
            user = CustomUser.objects.get(email=email)
            user.telegram_id = update.effective_user.id
            user.save()
            await update.message.reply_text(
                f"Успешно связал Телеграм с {email}!"
            )
        except CustomUser.DoesNotExist:
            await update.message.reply_text("Пользователь с таким email не найден.")

    async def echo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Я бот. Используй /start или /link <email>.")

    def handle(self, *args, **options):
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            self.stdout.write(self.style.ERROR(
                "TELEGRAM_BOT_TOKEN не установлен!"
            ))
            return

        async def main():
            app = ApplicationBuilder().token(token).build()

            app.add_handler(CommandHandler("start", self.start_command))
            app.add_handler(CommandHandler("link", self.link_command))
            app.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_message)
            )

            self.stdout.write(self.style.SUCCESS("Запуск бота (long-polling)..."))
            await app.run_polling()

        asyncio.run(main())
