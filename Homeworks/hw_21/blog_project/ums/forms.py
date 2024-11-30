# ---- Import Statements ----
import bleach
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from .models import UserProfile


# ---- Form Definitions ----

class LoginForm(forms.Form):
    """
    Define a login form with username and password fields.

    :var username: Username field with a text input widget.
    :var password: Password field with a password input widget.
    """

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


class RegistrationForm(forms.ModelForm):
    """
    Define a registration form for new users.

    :var username: Username field with validation for uniqueness.
    :var email: Email field with validation for uniqueness.
    :var password: Password field with password validation.
    :var confirm_password: Confirmation field for matching passwords.
    """

    username = forms.CharField(
        label='Username',
        max_length=50,
        help_text='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        help_text=''
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        """
        Meta options for RegistrationForm.

        :var model: The User model to associate with this form.
        :var fields: Fields to include in the form.
        """
        model = User
        fields = ('username',)

    def clean_password(self):
        """
        Validate the password against the password policies.

        :return: The cleaned password.
        :rtype: str
        """
        password = self.cleaned_data.get('password')
        validate_password(password, user=None)
        return password

    def clean_confirm_password(self):
        """
        Ensure the confirmation password matches the password.

        :return: The cleaned confirmation password.
        :rtype: str
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def clean_username(self):
        """
        Ensure the username is unique.

        :return: The cleaned username.
        :rtype: str
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        """
        Ensure the email address is unique.

        :return: The cleaned email address.
        :rtype: str
        """
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def save(self, commit=True):
        """
        Save the user instance with hashed password and create a UserProfile.

        :param commit: Whether to save the user instance immediately.
        :type commit: bool
        :return: The saved user instance.
        :rtype: User
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, email=self.cleaned_data['email'])
        return user


class ProfileEditForm(forms.ModelForm):
    """
    Define a form for editing user profiles.

    :var birth_date: Optional field for the user's birth date.
    """

    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        """
        Meta options for ProfileEditForm.

        :var model: The UserProfile model to associate with this form.
        :var fields: Fields to include in the form.
        """
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'location', 'avatar', 'bio']

    def clean_avatar(self):
        """
        Validate the size of the uploaded avatar.

        :return: The cleaned avatar field.
        :rtype: UploadedFile
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Image too large (>2 MBs)')
        return avatar

    def clean_bio(self):
        """
        Sanitize the bio content using bleach to allow specific HTML tags.

        :return: The cleaned bio content.
        :rtype: str
        """
        bio = self.cleaned_data.get('bio', '')
        allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'ol', 'li']
        bio = bleach.clean(bio, tags=allowed_tags, strip=True)
        return bio


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Extend the default PasswordChangeForm to add additional password validation.
    """

    def clean_new_password1(self):
        """
        Ensure the new password is not the same as the old password.

        :return: The cleaned new password.
        :rtype: str
        """
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        if old_password and new_password1 and new_password1 == old_password:
            raise forms.ValidationError('New password cannot be the same as current password')
        validate_password(new_password1, user=self.user)
        return new_password1
