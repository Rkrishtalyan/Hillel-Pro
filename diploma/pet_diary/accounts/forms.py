from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.html import format_html

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
            # 'avatar',
            # 'communication_method',
            # 'preferred_language',
            # 'preferred_timezone',
            'password1',
            'password2'
        )
        labels = {
            'email': _("Email"),
            'first_name': _("First Name"),
            'last_name': _("Last Name"),
            'phone_number': _("Phone Number"),
            'password1': _("Password"),
            'password2': _("Password confirmation"),
            # 'avatar': _("User Avatar"),
            # 'communication_method': _("Notification Method"),
            # 'preferred_language': _("Preferred Language"),
            # 'preferred_timezone': _("Preferred Timezone"),
        }
        help_texts = {
            'password1': _(
                "Your password can’t be too similar to your other personal information. "
                "Your password must contain at least 8 characters. "
                "Your password can’t be a commonly used password. "
                "Your password can’t be entirely numeric."
            ),
            'password2': _("Enter the same password as before, for verification."),
        }
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
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
            'communication_method': _("Notification Method"),
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
                format_html(
                    _(
                        "You cannot select Telegram as a communication method "
                        "because you do not have a Telegram ID. Please link your Telegram account first.<br>"
                        "Go to the link <a href='https://t.me/pet_bot_diary'>t.me/pet_bot_diary</a> and follow the instructions."
                    )
                )
            )
        return cleaned_data