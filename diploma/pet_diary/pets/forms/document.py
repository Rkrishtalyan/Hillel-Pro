from django import forms
from django.utils.translation import gettext_lazy as _

from pets.forms._widgets import DATE_WIDGET
from pets.models import PetDocument


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
