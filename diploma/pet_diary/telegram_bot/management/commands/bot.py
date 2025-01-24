import os
import logging
import pytz
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils import translation

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)

from accounts.models import CustomUser, CommunicationMethod
from pets.models import Task, Pet
from pets.notifications import _notify_owner_about_result


logging.basicConfig(level=logging.INFO)

CD_LINK = "LINK"
CD_MENU = "MENU"
CD_TASKS_MAIN = "TASKS_MAIN"
CD_SHOW_TODAY = "SHOW_TODAY"
CD_SHOW_PETS = "SHOW_PETS"
CD_SHOW_WEEK = "SHOW_WEEK"
CD_VIEW_TASK = "VIEW_TASK"
CD_MARK_DONE = "MARK_DONE"
CD_MARK_SKIP = "MARK_SKIP"
CD_PAGE_NEXT = "PAGE_NEXT"
CD_PAGE_PREV = "PAGE_PREV"
CD_BACK = "BACK"
SEPARATOR = "|"
CD_NOTIFY_DONE = "NOTIFY_DONE"
CD_NOTIFY_SKIP = "NOTIFY_SKIP"

LINKING_EMAIL = 1


class Command(BaseCommand):
    help = "Run Telegram bot (synchronous) with python-telegram-bot v13.x"

    @staticmethod
    def account_not_linked():
        return "Ви ще не привʼязали свій обліковий запис. Вмкористайте /start."

    def handle(self, *args, **options):
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            self.stderr.write("Error: TELEGRAM_BOT_TOKEN is not set!")
            return

        updater = Updater(token=token, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start_command))
        dp.add_handler(CommandHandler("tasks", self.tasks_command))

        link_conv_handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self.link_button_handler, pattern=f"^{CD_LINK}$")
            ],
            states={
                LINKING_EMAIL: [
                    MessageHandler(Filters.text & ~Filters.command, self.link_email_handler)
                ],
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel_link_handler)
            ],
            per_message=False,
        )
        dp.add_handler(link_conv_handler)

        dp.add_handler(CallbackQueryHandler(self.button_handler))

        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo_message))

        self.stdout.write(self.style.SUCCESS("Starting bot (long-polling)..."))
        updater.start_polling()
        updater.idle()

    def _activate_language(self, user):
        if user and user.preferred_language:
            translation.activate(user.preferred_language)
        else:
            translation.activate('ua')

    def _format_datetime(self, dt, user):
        if not dt:
            return _("No due date/time")
        if user and user.preferred_timezone:
            user_tz = pytz.timezone(user.preferred_timezone)
            local_dt = dt.astimezone(user_tz)
        else:
            local_dt = dt
        return local_dt.strftime("%Y-%m-%d %H:%M")

    def start_command(self, update: Update, context: CallbackContext):
        tg_id = update.effective_user.id
        user = self._get_user_by_tg(tg_id)
        self._activate_language(user)

        if user:
            text = _(f"Hello, %(user_name)s! Welcome to the bot menu.") % {
                'user_name': user.first_name
            }
            reply_markup = self._get_main_menu()
            update.message.reply_text(text, reply_markup=reply_markup)
        else:
            text = _("Вітаю! Ви ще не привʼязали свій обліковий запис.")
            keyboard = [[InlineKeyboardButton(_("Привʼязати"), callback_data=CD_LINK)]]
            update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    def tasks_command(self, update: Update, context: CallbackContext):
        tg_id = update.effective_user.id
        user = self._get_user_by_tg(tg_id)
        self._activate_language(user)

        if user:
            update.message.reply_text(
                _("Tasks menu"),
                reply_markup=self._get_tasks_menu()
            )
        else:
            update.message.reply_text(
                _(f"{self.account_not_linked()}")
            )

    def echo_message(self, update: Update, context: CallbackContext):
        tg_id = update.effective_user.id
        user = self._get_user_by_tg(tg_id)
        self._activate_language(user)

        update.message.reply_text(_("Вітаю! Оберіть /start щоб розпочати роботу."))

    def link_button_handler(self, update: Update, context: CallbackContext):
        query = update.callback_query
        tg_id = query.from_user.id
        user = self._get_user_by_tg(tg_id)
        self._activate_language(user)

        query.answer()

        if user:
            query.edit_message_text(
                text=_("You are already linked. Press /start for menu.")
            )
            return ConversationHandler.END

        query.edit_message_text(
            text=_("Будь ласка, введіть адресу електронної пошти (або введіть /cancel для скасування.):")
        )
        return LINKING_EMAIL

    def link_email_handler(self, update: Update, context: CallbackContext):
        tg_id = update.effective_user.id
        text = update.message.text.strip()
        try:
            user = CustomUser.objects.get(email=text)
            user.telegram_id = tg_id
            user.communication_method = CommunicationMethod.TELEGRAM
            user.save()
            self._activate_language(user)

            update.message.reply_text(_(f"Обліковий запис %(email)s успішно привʼязано до Telegram!") % {
                'email': user.email
            })
            main_menu = self._get_main_menu()
            update.message.reply_text(_("Now you can use menu button below"), reply_markup=main_menu)
        except CustomUser.DoesNotExist:
            update.message.reply_text(
                _("Користувача з такою адресою не знайдено. Будь ласка, спробуйте ще раз або введіть /cancel.")
            )
            return LINKING_EMAIL

        return ConversationHandler.END

    def cancel_link_handler(self, update: Update, context: CallbackContext):
        update.message.reply_text(_("Операцію скасовано. Оберіть /start щоб спробувати знову."))
        return ConversationHandler.END

    def button_handler(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        tg_id = query.from_user.id
        user = self._get_user_by_tg(tg_id)
        self._activate_language(user)

        data_str = query.data.strip()
        data = data_str.split(SEPARATOR)
        action = data[0].strip()
        params = data[1:] if len(data) > 1 else []

        if action == CD_MENU:
            if user:
                query.edit_message_text(
                    text=_("Main menu"),
                    reply_markup=self._get_main_menu()
                )
            else:
                query.edit_message_text(
                    text=_(f"{self.account_not_linked()}")
                )

        elif action == CD_TASKS_MAIN:
            if not user:
                query.edit_message_text(
                    text=_(f"{self.account_not_linked()}")
                )
            else:
                query.edit_message_text(
                    text=_("Tasks menu"),
                    reply_markup=self._get_tasks_menu()
                )

        elif action == CD_SHOW_TODAY:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            page = 0
            for p in params:
                if p.startswith("page="):
                    page = int(p.split("=")[1])
            self._show_today_tasks(query, user, page)

        elif action == CD_SHOW_PETS:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            page = 0
            for p in params:
                if p.startswith("page="):
                    page = int(p.split("=")[1])
            self._show_pets_list(query, user, page)

        elif action == CD_SHOW_WEEK:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            pet_id = None
            page = 0
            for p in params:
                if p.startswith("pet_id="):
                    pet_id = int(p.split("=")[1])
                elif p.startswith("page="):
                    page = int(p.split("=")[1])
            if not pet_id:
                query.edit_message_text(_("Pet not found."))
                return
            self._show_week_tasks(query, user, pet_id, page)

        elif action == CD_VIEW_TASK:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            task_id = None
            for p in params:
                if p.startswith("task_id="):
                    task_id = int(p.split("=")[1])
            self._view_task(query, user, task_id)

        elif action in [CD_MARK_DONE, CD_MARK_SKIP]:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            task_id = None
            for p in params:
                if p.startswith("task_id="):
                    task_id = int(p.split("=")[1])
            if not task_id:
                query.edit_message_text(_("Task not found."))
                return
            self._mark_task_status(query, user, task_id, action)

        elif action in [CD_NOTIFY_DONE, CD_NOTIFY_SKIP]:
            if not user:
                query.edit_message_text(_(f"{self.account_not_linked()}"))
                return
            task_id = None
            for p in params:
                if p.startswith("task_id="):
                    task_id = int(p.split("=")[1])
            if not task_id:
                query.edit_message_text(_("Task not found."))
                return

            self._mark_task_status_from_notification(query, user, task_id, action)

        elif action == CD_BACK:
            if user:
                query.edit_message_text(
                    text=_("Tasks menu"),
                    reply_markup=self._get_tasks_menu()
                )
            else:
                query.edit_message_text(_(f"{self.account_not_linked()}"))

        else:
            query.edit_message_text(_("Unknown action."))

    def _get_main_menu(self) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(_("Tasks"), callback_data=CD_TASKS_MAIN),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    def _get_tasks_menu(self) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(_("Tasks for today"), callback_data=CD_SHOW_TODAY),
            ],
            [
                InlineKeyboardButton(_("Tasks for specific Pet (7 days)"), callback_data=CD_SHOW_PETS),
            ],
            [
                InlineKeyboardButton(_("<- Back"), callback_data=CD_MENU)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def _show_today_tasks(self, query, user, page=0):
        today = timezone.localdate()
        tasks_qs = Task.objects.filter(
            pet__owner=user,
            deleted_at__isnull=True,
            status__in=[Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE]
        ).order_by('due_datetime')

        tasks_qs = [t for t in tasks_qs if t.due_datetime and t.due_datetime.date() == today]

        page_size = 5
        start = page * page_size
        end = start + page_size
        tasks_list = tasks_qs[start:end]
        total_count = len(tasks_qs)
        total_pages = max((total_count - 1) // page_size + 1, 1)

        text_lines = []
        text_lines.append(_("Tasks for today:"))
        text_lines.append(_("Page %(current_page)d of %(total_pages)d") % {
            'current_page': page + 1,
            'total_pages': total_pages
        })

        if page == 0:
            list_task_num = 1
        else:
            list_task_num = page_size + 1
        for t in tasks_list:
            dt_str = self._format_datetime(t.due_datetime, user)
            text_lines.append(f"{list_task_num}. {t.pet.name}: {t.title} ({dt_str})")
            list_task_num += 1

        text_to_show = "\n".join(text_lines)

        buttons = []
        if page == 0:
            button_task_num = 1
        else:
            button_task_num = page_size + 1
        for t in tasks_list:
            cb_data = f"{CD_VIEW_TASK}{SEPARATOR}task_id={t.id}"
            btn = InlineKeyboardButton(f"{button_task_num}. {t.title}", callback_data=cb_data)
            button_task_num += 1
            buttons.append([btn])

        nav_buttons = [InlineKeyboardButton(_("<- Back"), callback_data=CD_TASKS_MAIN)]
        if page > 0:
            prev_cb = f"{CD_SHOW_TODAY}{SEPARATOR}page={page-1}"
            nav_buttons.append(InlineKeyboardButton("←", callback_data=prev_cb))
        if end < total_count:
            next_cb = f"{CD_SHOW_TODAY}{SEPARATOR}page={page+1}"
            nav_buttons.append(InlineKeyboardButton("→", callback_data=next_cb))

        keyboard = buttons
        if nav_buttons:
            keyboard.append(nav_buttons)

        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=text_to_show, reply_markup=markup)

    def _show_pets_list(self, query, user, page=0):
        pets_qs = Pet.objects.filter(models.Q(owner=user) | models.Q(caregiver=user)).order_by('name')
        page_size = 8
        start = page * page_size
        end = start + page_size
        total_count = pets_qs.count()
        total_pages = max((total_count - 1) // page_size + 1, 1)

        pets_list = pets_qs[start:end]

        text_lines = []
        text_lines.append(_("Select a Pet:"))
        text_lines.append(_("Page %(current_page)d of %(total_pages)d") % {
            'current_page': page + 1,
            'total_pages': total_pages
        })
        for p in pets_list:
            text_lines.append(f"- {p.name}")

        keyboard = []
        for p in pets_list:
            cb_data = f"{CD_SHOW_WEEK}{SEPARATOR}pet_id={p.id}{SEPARATOR}page=0"
            btn = InlineKeyboardButton(p.name, callback_data=cb_data)
            keyboard.append([btn])

        nav_buttons = [InlineKeyboardButton(_("<- Back"), callback_data=CD_TASKS_MAIN)]
        if page > 0:
            prev_cb = f"{CD_SHOW_PETS}{SEPARATOR}page={page-1}"
            nav_buttons.append(InlineKeyboardButton("←", callback_data=prev_cb))
        if end < total_count:
            next_cb = f"{CD_SHOW_PETS}{SEPARATOR}page={page+1}"
            nav_buttons.append(InlineKeyboardButton("→", callback_data=next_cb))

        if nav_buttons:
            keyboard.append(nav_buttons)

        query.edit_message_text(
            text="\n".join(text_lines),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def _show_week_tasks(self, query, user, pet_id, page=0):
        now_utc = timezone.now().date()
        week_later_utc = now_utc + timedelta(days=7)

        tasks_qs = Task.objects.filter(
            pet_id=pet_id,
            deleted_at__isnull=True,
            status__in=[Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE],
            due_datetime__range=(now_utc, week_later_utc)
        ).order_by('due_datetime')

        page_size = 5
        start = page * page_size
        end = start + page_size
        total_count = tasks_qs.count()
        total_pages = max((total_count - 1) // page_size + 1, 1)

        tasks_list = tasks_qs[start:end]

        text_lines = []
        try:
            pet_obj = Pet.objects.get(id=pet_id, owner=user)
            text_lines.append(_(f"Tasks for pet: %(pet_name)s (next 7 days)") % {
                'pet_name': pet_obj.name,
            }
            )
        except Pet.DoesNotExist:
            text_lines.append(_("Pet not found for you."))

        text_lines.append(_("Page %(current_page)d of %(total_pages)d") % {
            'current_page': page + 1,
            'total_pages': total_pages
        })

        if page == 0:
            list_task_num = 1
        else:
            list_task_num = page_size + 1
        for t in tasks_list:
            dt_str = self._format_datetime(t.due_datetime, user)
            text_lines.append(f"{list_task_num}. {t.title} ({dt_str})")
            list_task_num += 1

        text_to_show = "\n".join(text_lines)

        keyboard = []
        if page == 0:
            button_task_num = 1
        else:
            button_task_num = page_size + 1
        for t in tasks_list:
            cb_data = f"{CD_VIEW_TASK}{SEPARATOR}task_id={t.id}"
            btn = InlineKeyboardButton(f"{button_task_num}. {t.title}", callback_data=cb_data)
            keyboard.append([btn])
            button_task_num += 1

        nav_buttons = []

        back_cb = f"{CD_SHOW_PETS}{SEPARATOR}page=0"
        nav_buttons.append(InlineKeyboardButton(_("<- Back"), callback_data=back_cb))

        if page > 0:
            prev_cb = f"{CD_SHOW_WEEK}{SEPARATOR}pet_id={pet_id}{SEPARATOR}page={page-1}"
            nav_buttons.append(InlineKeyboardButton("←", callback_data=prev_cb))
        if end < total_count:
            next_cb = f"{CD_SHOW_WEEK}{SEPARATOR}pet_id={pet_id}{SEPARATOR}page={page+1}"
            nav_buttons.append(InlineKeyboardButton("→", callback_data=next_cb))

        if nav_buttons:
            keyboard.append(nav_buttons)

        query.edit_message_text(
            text=text_to_show,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def _view_task(self, query, user, task_id):
        try:
            task = Task.objects.get(id=task_id, deleted_at__isnull=True)
        except Task.DoesNotExist:
            query.edit_message_text(_("Task not found or deleted."))
            return

        status = task.status
        dt_str = self._format_datetime(task.due_datetime, user)

        msg_lines = [
            f"{_('Pet')}: {task.pet.name}",
            f"{_('Task')}: {task.title}",
            f"{_('Due')}: {dt_str}",
            f"{_('Status')}: {status}",
        ]

        if status not in [Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE]:
            msg_lines.append(_("This task is not active. You cannot change it."))
            text = "\n".join(msg_lines)
            keyboard = [[InlineKeyboardButton(_("<- Back"), callback_data=CD_TASKS_MAIN)]]
            query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

        text = "\n".join(msg_lines)
        done_cb = f"{CD_MARK_DONE}{SEPARATOR}task_id={task.id}"
        skip_cb = f"{CD_MARK_SKIP}{SEPARATOR}task_id={task.id}"

        back_cb = CD_TASKS_MAIN
        keyboard = [
            [
                InlineKeyboardButton(_("Done"), callback_data=done_cb),
                InlineKeyboardButton(_("Skipped"), callback_data=skip_cb),
            ],
            [
                InlineKeyboardButton(_("<- Back"), callback_data=back_cb)
            ]
        ]
        query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

    def _mark_task_status(self, query, user, task_id, action):
        try:
            task = Task.objects.get(id=task_id, deleted_at__isnull=True)
        except Task.DoesNotExist:
            query.edit_message_text(_("Task not found or deleted."))
            return

        if task.status not in [Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE]:
            query.edit_message_text(
                _(f"Task already has status %(task.status)s. Cannot change.") % {
                    'status': task.status
                }
            )
            return

        keyboard = [[InlineKeyboardButton(_("<- Back"), callback_data=CD_TASKS_MAIN)]]

        if action == CD_MARK_DONE:
            task.mark_as_done(user)
            task.save()
            query.edit_message_text(
                _("Task marked as done."),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            task.mark_as_skipped(user)
            task.save()
            query.edit_message_text(
                _("Task marked as skipped."),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    def _get_user_by_tg(self, tg_id):
        try:
            return CustomUser.objects.get(telegram_id=tg_id)
        except CustomUser.DoesNotExist:
            return None

    def _mark_task_status_from_notification(self, query, user, task_id, action):
        try:
            task = Task.objects.get(id=task_id, deleted_at__isnull=True)
        except Task.DoesNotExist:
            query.edit_message_text(_("Task not found or deleted."))
            return

        if task.status not in [Task.TaskStatus.PLANNED, Task.TaskStatus.OVERDUE]:
            query.edit_message_text(
                _(f"Task already has status %(task.status)s. Cannot change.") % {
                    'status': task.status
                }
            )
            return

        if action == CD_NOTIFY_DONE:
            task.mark_as_done(user)
            task.save()
            result_text = _(f"Task '%(task)s' marked as done.") % {
                'task': task.title
            }
        else:
            task.mark_as_skipped(user)
            task.save()
            result_text = _(f"Task '%(task)s' marked as skipped.") % {
                'task': task.title
            }
        query.edit_message_reply_markup(reply_markup=None)
        query.edit_message_text(text=result_text)
