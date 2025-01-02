from .models import URL
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class URLForm(forms.ModelForm):
    """
    Represent a form for creating or editing a URL model instance.

    This form allows users to input the original URL to be shortened.

    :Meta attribute model: The model associated with this form.
    :Meta attribute fields: Specifies the fields to include in the form.
    """
    class Meta:
        model = URL
        fields = ('original_url',)


class RegistrationForm(UserCreationForm):
    """
    Represent a user registration form with additional email field.

    This form extends the default Django UserCreationForm by adding an email
    field as a required input during user registration.

    :var email: A required email field for user registration.
    :type email: EmailField

    :Meta attribute model: The user model associated with this form.
    :Meta attribute fields: Specifies the fields to include in the form.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
