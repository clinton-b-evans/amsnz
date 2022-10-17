from django.forms import ModelForm
from .models import Crypto
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class CryptoForm(ModelForm):
    class Meta:
        model = Crypto
        fields = "__all__"
