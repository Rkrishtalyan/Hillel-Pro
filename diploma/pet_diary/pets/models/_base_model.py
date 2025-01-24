from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET('User deleted'),
        related_name='%(app_label)s_%(class)s_created',
        verbose_name=_("Created by"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )
    edited_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Edited at")
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_edited',
        verbose_name=_("Edited by")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Deleted at")
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_deleted',
        verbose_name=_("Deleted by")
    )

    class Meta:
        abstract = True

    def mark_as_edited(self, user):
        self.edited_at = timezone.now()
        self.edited_by = user
        self.updated_by = user

    def mark_as_deleted(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.updated_by = user
