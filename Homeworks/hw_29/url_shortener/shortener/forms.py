from .models import URL
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('original_url',)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')