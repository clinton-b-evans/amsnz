from django.forms import ModelForm
from .models import Property
from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = "date"


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

