from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel
from pets.models.pet import Pet


class Task(BaseModel):

    class TaskStatus(models.TextChoices):
        PLANNED = 'planned', _("Planned")
        OVERDUE = 'overdue', _("Overdue")
        DONE = 'done', _("Done")
        SKIPPED = 'skipped', _("Skipped")

    REMIND_BEFORE_CHOICES = [
        ('15_min', _("15 minutes")),
        ('1_hour', _("1 hour")),
        ('4_hours', _("4 hours")),
        ('12_hours', _("12 hours")),
        ('1_day', _("1 day")),
        ('3_days', _("3 days")),
        ('1_week', _("1 week")),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_("Pet")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title")
    )
    due_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Due Date and Time")
    )
    remind_me = models.BooleanField(
        default=False,
        verbose_name=_("Remind Me")
    )
    remind_before = models.CharField(
        max_length=20,
        choices=REMIND_BEFORE_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Remind Before")
    )
    status = models.CharField(
        max_length=10,
        choices=TaskStatus.choices,
        default=TaskStatus.PLANNED,
        verbose_name=_("Status")
    )
    recurring = models.BooleanField(
        default=False,
        verbose_name=_("Recurring?")
    )
    recurring_days = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Number of days to repeat")
    )
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_("Reminder Sent")
    )
    reminder_sent_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Reminder Sent at")
    )
    reminder_sent_with = models.CharField(
        max_length=20,
        blank=True,
    )

    skipped_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Skipped at"))
    skipped_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='skipped_tasks',
        verbose_name=_("Skipped By")
    )

    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Completed at"))
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='completed_tasks',
        verbose_name=_("Completed By")
    )

    # def mark_as_edited(self, user):
    #     super().mark_as_edited(user)

    # def mark_as_deleted(self, user):
    #     super().mark_as_deleted(user)

    def mark_as_skipped(self, user):
        self.status = self.TaskStatus.SKIPPED
        self.skipped_at = timezone.now()
        self.skipped_by = user

    def mark_as_done(self, user):
        self.status = self.TaskStatus.DONE
        self.completed_at = timezone.now()
        self.completed_by = user

    def mark_as_reminded_via_email(self):
        self.reminder_sent = True
        self.reminder_sent_at = timezone.now()
        self.reminder_sent_with = 'email'

    def mark_as_reminded_via_telegram(self):
        self.reminder_sent = True
        self.reminder_sent_at = timezone.now()
        self.reminder_sent_with = 'telegram'

    def __str__(self):
        return f"{self.title} (pet={self.pet.name}, status={self.status})"

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
