import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext
)

from accounts.models import CustomUser, CommunicationMethod
from pets.models import Task
from pets.notifications import _notify_owner_about_result


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):

    help = "Run Telegram bot (synchronous) with python-telegram-bot v13.x"

    def handle(self, *args, **options):
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            self.stderr.write("Error: TELEGRAM_BOT_TOKEN is not set!")
            return

        updater = Updater(token=token, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start_command))
        dp.add_handler(CommandHandler("link", self.link_command))
        dp.add_handler(CallbackQueryHandler(self.button_handler))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo_message))

        self.stdout.write(self.style.SUCCESS("Starting bot (long-polling)..."))
        updater.start_polling()
        updater.idle()

    # ---- Handlers ----

    def start_command(self, update: Update, context: CallbackContext):
        user = self._get_user_by_tg(update.effective_user.id)
        if user:
            reply = _(f"Hello, {user.first_name}! You are linked.")
        else:
            reply = _("Hello! You have not linked an account yet.")

        keyboard = [
            [
                InlineKeyboardButton(
                    text=_("Link account"), callback_data="LINK"
                ),
                InlineKeyboardButton(
                    text=_("Show tasks"), callback_data="SHOW_TASKS"
                ),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply, reply_markup=markup)

    def link_command(self, update: Update, context: CallbackContext):
        args = context.args
        if not args:
            update.message.reply_text(_("Usage: /link <email>"))
            return
        email = args[0]

        try:
            user = CustomUser.objects.get(email=email)
            user.telegram_id = update.effective_user.id
            user.communication_method = CommunicationMethod.TELEGRAM
            user.save()
            update.message.reply_text(
                _(f"Successfully linked Telegram with {email}!")
            )
        except CustomUser.DoesNotExist:
            update.message.reply_text(
                _("User with this email not found.")
            )

    def echo_message(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            _("I am a bot. Use /start or /link <email>.")
        )

    def button_handler(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        user = self._get_user_by_tg(query.from_user.id)

        if query.data == "LINK":
            query.message.reply_text(
                _("Use /link <email> to link your account.")
            )

        elif query.data == "SHOW_TASKS":
            if not user:
                query.message.reply_text(
                    _("You have not linked an account yet. Use /link <email>.")
                )
                return

            tasks = Task.objects.filter(
                pet__owner=user
            ).order_by('due_datetime')[:3]

            if not tasks:
                query.message.reply_text(_("You have no tasks."))
                return

            for t in tasks:
                text_for_task = self._format_task_text(t)
                kb = [
                    [
                        InlineKeyboardButton(_("Done"), callback_data=f"DONE:{t.id}"),
                        InlineKeyboardButton(_("Skipped"), callback_data=f"SKIP:{t.id}"),
                    ]
                ]
                markup = InlineKeyboardMarkup(kb)
                query.message.reply_text(text_for_task, reply_markup=markup)

        elif query.data.startswith("DONE:") or query.data.startswith("SKIP:"):
            parts = query.data.split(":")
            action = parts[0]  # DONE or SKIP
            task_id = parts[1]

            try:
                task = Task.objects.get(id=task_id, deleted_at__isnull=True)
            except Task.DoesNotExist:
                query.message.reply_text(_("Task not found."))
                return

            user = self._get_user_by_tg(query.from_user.id)
            old_status = task.status

            if action == "DONE":
                task.mark_as_done(user)
                task.save()
                query.message.reply_text(_("Task marked as done."))

            else:
                task.mark_as_skipped(user)
                task.save()
                query.message.reply_text(_("Task marked as skipped."))
        else:
            query.message.reply_text(_("Unknown action."))

    # ---- Utils ----
    def _get_user_by_tg(self, tg_id):
        try:
            return CustomUser.objects.get(telegram_id=tg_id)
        except CustomUser.DoesNotExist:
            return None

    def _format_task_text(self, t: Task) -> str:
        if t.due_datetime:
            return _(f"Task: {t.title}\nDue: {t.due_datetime}")
        else:
            return _(f"Task: {t.title}\nNo due date/time")
