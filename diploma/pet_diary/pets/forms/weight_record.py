from django import forms
from django.utils.translation import gettext_lazy as _

from pets.forms._widgets import DATE_WIDGET
from pets.models import WeightRecord


class WeightRecordForm(forms.ModelForm):
    date = forms.DateField(
        widget=DATE_WIDGET,
        label=_("Date")
    )

    class Meta:
        model = WeightRecord
        fields = ['date', 'weight_kg']
        labels = {
            'weight_kg': _("Weight (kg)"),
        }
