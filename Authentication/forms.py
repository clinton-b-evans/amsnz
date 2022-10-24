from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Authentication.models import ContactUs


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["name", "email", "subject", "message"]
