from django import forms
from django.utils.translation import gettext_lazy as _

from pets.models import PetImage


class PetImageForm(forms.ModelForm):
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label=_("Notes")
    )

    class Meta:
        model = PetImage
        fields = ['path', 'notes']
        labels = {
            'path': _("Photo"),
            'notes': _("Notes"),
        }
        widgets = {
            'path': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
