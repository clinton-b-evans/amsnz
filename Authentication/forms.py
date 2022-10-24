from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Authentication.models import ContactUs


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        data = self.cleaned_data.get("username")
        if "@" in data:
            raise forms.ValidationError("Contains @")
        return data


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["name", "email", "subject", "message"]
