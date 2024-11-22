# ---- Standard Library Imports ----
import bleach

# ---- Third-Party Imports ----
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput

# ---- Local Imports ----
from .models import UserProfile


# ---- Login Form Definition ----
class LoginForm(forms.Form):
    """
    Represent a login form for user authentication.

    :var username: The username of the user.
    :type username: str
    :var password: The password of the user.
    :type password: str
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# ---- Registration Form Definition ----
class RegistrationForm(forms.ModelForm):
    """
    Represent a registration form for creating a new user.

    :var username: The desired username of the user.
    :type username: str
    :var password: The password of the user.
    :type password: str
    :var password_confirm: Password confirmation for verification.
    :type password_confirm: str
    :var email: The email address of the user.
    :type email: str
    """
    username = forms.CharField(
        max_length=150,
        help_text='',
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='',
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        """
        Validate the password using Django's password validation.
        """
        password = self.cleaned_data.get('password')
        validate_password(password, user=None)
        return password

    def clean_password_confirm(self):
        """
        Ensure the password confirmation matches the password.
        """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match.")
        return password_confirm

    def clean_username(self):
        """
        Ensure the username does not already exist.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username

    def clean_email(self):
        """
        Ensure the email is not already in use.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already in use.')
        return email

    def save(self, commit=True):
        """
        Save the user instance with an encrypted password.

        :param commit: Whether to commit the save to the database.
        :type commit: bool
        :return: The saved user instance.
        :rtype: User
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ---- User Profile Form Definition ----
class UserProfileForm(forms.ModelForm):
    """
    Represent a form for editing user profile details.

    :var birth_date: The user's birth date.
    :type birth_date: date
    :var bio: A short biography for the user.
    :type bio: str
    :var location: The user's location.
    :type location: str
    :var avatar: A profile picture for the user.
    :type avatar: ImageField
    """
    birth_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']

    def clean_avatar(self):
        """
        Validate the avatar file size.
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Image file too large ( > 2MB ).")
        return avatar

    def clean_bio(self):
        """
        Clean and sanitize the bio field for allowed HTML tags.

        :return: The sanitized bio content.
        :rtype: str
        """
        bio = self.cleaned_data.get('bio', '')
        allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'ol', 'li']
        bio = bleach.clean(bio, tags=allowed_tags, strip=True)
        return bio


# ---- Custom Password Change Form ----
class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Represent a custom form for changing a user's password.

    Inherits from Django's PasswordChangeForm.
    """

    def clean_new_password1(self):
        """
        Ensure the new password is different from the old password.

        :return: The validated new password.
        :rtype: str
        """
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        if old_password and new_password1 and old_password == new_password1:
            raise ValidationError("New password must be different from the current password.")
        validate_password(new_password1, user=self.user)
        return new_password1
