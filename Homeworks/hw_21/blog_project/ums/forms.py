import bleach
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=50, help_text='')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='')
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password, user=None)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'location', 'avatar', 'bio']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Image too large (>2 MBs)')
        return avatar

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '')
        allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'ol', 'li']
        bio = bleach.clean(bio, tags=allowed_tags, strip=True)
        return bio


class CustomPasswordChangeForm(PasswordChangeForm):

    def clean_new_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        if old_password and new_password1 and new_password1 == old_password:
            raise forms.ValidationError('New password cannot be the same as current password')
        validate_password(new_password1, user=self.user)
        return new_password1
