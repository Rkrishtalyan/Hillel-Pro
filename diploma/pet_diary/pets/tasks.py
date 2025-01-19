import os
import pytz
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from pets.models import Task
from accounts.models import CustomUser


_bot = None


def get_bot() -> Bot:
    global _bot
    if _bot is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        _bot = Bot(token=token)
    return _bot


@shared_task
def check_tasks_for_reminders():
    now_utc = timezone.now()
    tasks_qs = Task.objects.filter(
        remind_me=True,
        status__in=['planned', 'overdue'],
        reminder_sent=False,
        due_datetime__isnull=False,
        deleted_at__isnull=True
    )
    for t in tasks_qs:
        offset = _parse_remind_before(t.remind_before)
        remind_moment_utc = t.due_datetime - offset

        if remind_moment_utc <= now_utc < t.due_datetime:
            user = t.pet.caregiver if t.pet.caregiver else t.pet.owner
            _send_task_reminder(user, t)
            t.save()


def _parse_remind_before(rb: str) -> timedelta:
    if rb == '15_min':
        return timedelta(minutes=15)
    elif rb == '1_hour':
        return timedelta(hours=1)
    elif rb == '4_hours':
        return timedelta(hours=4)
    elif rb == '12_hours':
        return timedelta(hours=12)
    elif rb == '1_day':
        return timedelta(days=1)
    elif rb == '3_days':
        return timedelta(days=3)
    elif rb == '1_week':
        return timedelta(weeks=1)
    return timedelta(0)


def _send_task_reminder(user: CustomUser, task: Task):
    msg_text = f"Reminder: Task '{task.title}' is due at {task.due_datetime}!"
    keyboard = [
        [
            InlineKeyboardButton("Done", callback_data=f"DONE:{task.id}"),
            InlineKeyboardButton("Skipped", callback_data=f"SKIP:{task.id}"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if user.communication_method == 'telegram' and user.telegram_id:
        bot = get_bot()
        bot.send_message(
            chat_id=user.telegram_id,
            text=msg_text,
            reply_markup=markup
        )
        task.mark_as_reminded_via_telegram()
    else:
        from django.core.mail import send_mail
        send_mail(
            subject="Task Reminder",
            message=msg_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        task.mark_as_reminded_via_email()
