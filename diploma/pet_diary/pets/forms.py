from django import forms
from django.utils.translation import gettext_lazy as _
from pets.models import (
    Pet,
    WeightLog,
    PetImage,
    VaccinationLog,
    Task,
    PetDocument
)


DATE_WIDGET = forms.DateInput(attrs={'type': 'date'})
TIME_WIDGET = forms.TimeInput(attrs={'type': 'time'})


# -------------------------------
#           PetForm
# -------------------------------
class PetForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=DATE_WIDGET,
        label=_("Birth Date")
    )

    class Meta:
        model = Pet
        fields = [
            'name',
            'species',
            'birth_date',
            'breed',
            'chip_number',
            'avatar',
            'notes',
            'confirmed_diagnoses',
            'current_prescriptions',
        ]
        labels = {
            'name': _("Pet Name"),
            'species': _("Species"),
            'breed': _("Breed"),
            'chip_number': _("Chip Number"),
            'avatar': _("Avatar"),
            'notes': _("Notes"),
            'confirmed_diagnoses': _("Confirmed Diagnoses"),
            'current_prescriptions': _("Current Prescriptions"),
        }


# -------------------------------
#         WeightLogForm
# -------------------------------
class WeightLogForm(forms.ModelForm):
    date = forms.DateField(
        widget=DATE_WIDGET,
        label=_("Date")
    )

    class Meta:
        model = WeightLog
        fields = ['date', 'weight_kg']
        labels = {
            'weight_kg': _("Weight (kg)"),
        }


# -------------------------------
#       PetImageForm
# -------------------------------
class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']
        labels = {
            'image': _("Photo"),
        }


# -------------------------------
#    VaccinationLogForm
# -------------------------------
class VaccinationLogForm(forms.ModelForm):
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
        model = VaccinationLog
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


# -------------------------------
#        TaskCreateForm
# -------------------------------
class TaskCreateForm(forms.ModelForm):
    due_datetime = forms.DateTimeField(
        required=False,
        label=_("Due DateTime"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Task
        fields = [
            'title',
            'due_datetime',
            'remind_me',
            'remind_before',
            'status',
            'recurring',
            'recurring_days',
        ]
        labels = {
            'title':          _("Title"),
            'due_datetime':   _("Due Date/Time"),
            'remind_me':      _("Remind Me"),
            'remind_before':  _("Remind Before"),
            'status':         _("Status"),
            'recurring':      _("Recurring?"),
            'recurring_days': _("Number of days to repeat"),
        }


# -------------------------------
#        TaskEditForm
# -------------------------------
class TaskEditForm(forms.ModelForm):
    due_datetime = forms.DateTimeField(
        required=False,
        label=_("Due DateTime"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Task
        # Excluding recurring and recurring_days
        exclude = ['recurring', 'recurring_days', 'pet', 'created_at', 'updated_at']
        labels = {
            'title':         _("Title"),
            'due_datetime':  _("Due Date/Time"),
            'remind_me':     _("Remind Me"),
            'remind_before': _("Remind Before"),
            'status':        _("Status"),
        }


# -------------------------------
#     PetDocumentForm
# -------------------------------
class PetDocumentForm(forms.ModelForm):
    doc_date = forms.DateField(
        widget=DATE_WIDGET,
        label=_("Document Date")
    )

    class Meta:
        model = PetDocument
        fields = ['doc_file', 'doc_type', 'doc_date', 'description']
        labels = {
            'doc_file': _("Document File"),
            'doc_type': _("Document Type"),
            'description': _("Description"),
        }
