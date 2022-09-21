from django.forms import ModelForm
from .models import PersonalBalance
from django import forms

class PersonalBalanceForm(ModelForm):
    class Meta:
        model = PersonalBalance
        fields = '__all__'
