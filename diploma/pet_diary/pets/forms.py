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


class PetForm(forms.ModelForm):
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
            'birth_date': _("Birth Date"),
            'breed': _("Breed"),
            'chip_number': _("Chip Number"),
            'avatar': _("Avatar"),
            'notes': _("Notes"),
            'confirmed_diagnoses': _("Confirmed Diagnoses"),
            'current_prescriptions': _("Current Prescriptions"),
        }


class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight_kg']
        labels = {
            'date': _("Date"),
            'weight_kg': _("Weight (kg)"),
        }


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']
        labels = {
            'image': _("Photo"),
        }


class VaccinationLogForm(forms.ModelForm):
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
            'date_administered': _("Date Administered"),
            'next_due_date': _("Next Due Date"),
            'notes': _("Notes"),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'done']
        labels = {
            'title': _("Title"),
            'due_date': _("Due Date"),
            'done': _("Done"),
        }


class PetDocumentForm(forms.ModelForm):
    class Meta:
        model = PetDocument
        fields = ['doc_file', 'doc_type', 'doc_date', 'description']
        labels = {
            'doc_file': _("Document File"),
            'doc_type': _("Document Type"),
            'doc_date': _("Document Date"),
            'description': _("Description"),
        }
