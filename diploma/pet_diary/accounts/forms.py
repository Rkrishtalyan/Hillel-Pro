from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')
        labels = {
            'email': _("Email"),
            'first_name': _("First Name"),
            'last_name': _("Last Name"),
            'phone_number': _("Phone Number"),
        }
