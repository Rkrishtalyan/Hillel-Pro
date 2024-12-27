from .models import URL
from django import forms


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('original_url',)
