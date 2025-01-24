from django import forms
from django.utils.translation import gettext_lazy as _

from pets.models import Task


class TaskCreateForm(forms.ModelForm):
    due_datetime = forms.DateTimeField(
        required=False,
        label=_("Due DateTime"),
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Task
        fields = [
            'title',
            'due_datetime',
            'remind_me',
            'remind_before',
            # 'status',
            'recurring',
            'recurring_days',
        ]
        labels = {
            'title':          _("Title"),
            'due_datetime':   _("Due Date/Time"),
            'remind_me':      _("Remind Me"),
            'remind_before':  _("Remind Before"),
            # 'status':         _("Status"),
            'recurring':      _("Recurring?"),
            'recurring_days': _("Number of days to repeat"),
        }


class TaskEditForm(forms.ModelForm):
    due_datetime = forms.DateTimeField(
        required=False,
        label=_("Due DateTime"),
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
    )

    class Meta:
        model = Task
        fields = [
            'title',
            'due_datetime',
            'remind_me',
            'remind_before',
            'status'
        ]
        labels = {
            'title':         _("Title"),
            'due_datetime':  _("Due Date/Time"),
            'remind_me':     _("Remind Me"),
            'remind_before': _("Remind Before"),
            'status':        _("Status"),
        }
