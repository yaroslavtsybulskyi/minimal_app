from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    """
    A form registering new user. Inherits from UserCreationForm and
    adds an email field.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    """
    A form for logging in.
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
