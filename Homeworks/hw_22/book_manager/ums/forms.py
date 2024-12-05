from django import forms


# ---- Login Form ----
class LoginForm(forms.Form):
    """
    Form for user login with name and age fields.

    Attributes:
        name (CharField): The name of the user, limited to 100 characters.
        age (IntegerField): The age of the user, must be non-negative.
    """
    name = forms.CharField(max_length=100, label='Name')
    age = forms.IntegerField(min_value=0, label='Age')
