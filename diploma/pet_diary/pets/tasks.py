import os
import pytz
from datetime import timedelta
from celery import shared_task
from django.utils import timezone, translation
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from pets.models import Task
from accounts.models import CustomUser, CommunicationMethod


_bot = None

CD_NOTIFY_DONE = "NOTIFY_DONE"
CD_NOTIFY_SKIP = "NOTIFY_SKIP"
SEPARATOR = "|"


def _activate_language(user):
    if user and user.preferred_language:
        translation.activate(user.preferred_language)
    else:
        translation.activate('ua')


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
        status__in=[Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE],
        reminder_sent=False,
        due_datetime__isnull=False,
        deleted_at__isnull=True
    )
    for t in tasks_qs:
        offset = _parse_remind_before(t.remind_before)
        remind_moment_utc = t.due_datetime - offset

        if remind_moment_utc <= now_utc < t.due_datetime:
            user = t.pet.caregiver if t.pet.caregiver else t.pet.owner
            if user:
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


def _send_task_reminder(user, task):
    _activate_language(user)
    due_str = _format_datetime_for_user(task.due_datetime, user)
    msg_text = _(
    "Reminder: Task '%(task_title)s' for pet %(pet_name)s is due at %(due_datetime)s!"
) % {
    'task_title': task.title,
    'pet_name': task.pet.name,
    'due_datetime': due_str,
}

    callback_done = f"{CD_NOTIFY_DONE}{SEPARATOR}task_id={task.id}"
    callback_skip = f"{CD_NOTIFY_SKIP}{SEPARATOR}task_id={task.id}"
    keyboard = [
        [
            InlineKeyboardButton(_("Done"), callback_data=callback_done),
            InlineKeyboardButton(_("Skip"), callback_data=callback_skip),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if user.communication_method == CommunicationMethod.TELEGRAM and user.telegram_id:
        bot = get_bot()
        bot.send_message(
            chat_id=user.telegram_id,
            text=msg_text,
            reply_markup=markup
        )
        task.mark_as_reminded_via_telegram()
    else:
        send_mail(
            subject=_("Task Reminder"),
            message=msg_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        task.mark_as_reminded_via_email()


def _format_datetime_for_user(dt, user):
    if not dt:
        return "N/A"

    if user and user.preferred_timezone:
        try:
            user_tz = pytz.timezone(user.preferred_timezone)
            local_dt = dt.astimezone(user_tz)
        except Exception:
            local_dt = dt
    else:
        local_dt = dt
    return local_dt.strftime("%Y-%m-%d %H:%M")
