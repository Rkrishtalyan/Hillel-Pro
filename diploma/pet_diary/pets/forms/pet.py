from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from pets.forms._widgets import DATE_WIDGET
from pets.models import Pet


class PetForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=DATE_WIDGET,
        label=_("Birth Date")
    )
    caregiver_email = forms.EmailField(
        required=False,
        label=_("Caregiver Email"),
        help_text=_("Enter email of the user to assign as caregiver. Leave blank to clear.")
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
            'ration',
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
            'ration': _("Ration"),
            'confirmed_diagnoses': _("Confirmed Diagnoses"),
            'current_prescriptions': _("Current Prescriptions"),
        }

    def save(self, commit=True):
        pet = super().save(commit=False)
        caregiver_email = self.cleaned_data.get('caregiver_email', '').strip()

        if caregiver_email:
            try:
                user = CustomUser.objects.get(email=caregiver_email)
                pet.caregiver = user
            except CustomUser.DoesNotExist:
                raise ValidationError(
                    _("User with email %(email)s not found."),
                    code='invalid',
                    params={'email': caregiver_email},
                )
        else:
            pet.caregiver = None

        if commit:
            pet.save()
        return pet
