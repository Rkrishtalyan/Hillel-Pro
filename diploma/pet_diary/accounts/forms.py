from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from accounts.models import CommunicationMethod


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'communication_method',
            'preferred_language',
            'preferred_timezone',
            'password1',
            'password2'
        )
        labels = {
            'email': _("Email"),
            'first_name': _("First Name"),
            'last_name': _("Last Name"),
            'phone_number': _("Phone Number"),
            'avatar': _("User Avatar"),
            'communication_method': _("Preferred Communication Method"),
            'preferred_language': _("Preferred Language"),
            'preferred_timezone': _("Preferred Timezone"),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'communication_method',
            # 'preferred_language',
            # 'preferred_timezone',
        )
        labels = {
            'first_name': _("First Name"),
            'last_name': _("Last Name"),
            'phone_number': _("Phone Number"),
            'avatar': _("User Avatar"),
            'communication_method': _("Preferred Communication Method"),
            'preferred_language': _("Preferred Language"),
            'preferred_timezone': _("Preferred Timezone"),
        }

    def clean(self):
        cleaned_data = super().clean()
        comm_method = cleaned_data.get('communication_method')
        telegram_id = self.instance.telegram_id
        if comm_method == CommunicationMethod.TELEGRAM and not telegram_id:
            self.add_error(
                'communication_method',
                _("You cannot select Telegram as communication method "
                  "because you have no Telegram ID. Please link your Telegram first.")
            )
        return cleaned_data
