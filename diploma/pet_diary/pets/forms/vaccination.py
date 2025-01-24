from django import forms
from django.utils.translation import gettext_lazy as _

from pets.forms._widgets import DATE_WIDGET
from pets.models import Vaccination


class VaccinationForm(forms.ModelForm):
    date_administered = forms.DateField(
        widget=DATE_WIDGET,
        label=_("Date Administered"),
        required=True
    )
    next_due_date = forms.DateField(
        widget=DATE_WIDGET,
        label=_("Next Due Date"),
        required=False
    )

    class Meta:
        model = Vaccination
        fields = [
            'vaccine_name',
            'date_administered',
            'next_due_date',
            'notes',
        ]
        labels = {
            'vaccine_name': _("Vaccine Name"),
            'notes': _("Notes"),
        }
