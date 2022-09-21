from django.forms import ModelForm
from .models import IncomeStatement, Category
from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = 'date'

class IncomeStatementForm(ModelForm):
    class Meta:
        model = IncomeStatement
        fields = '__all__'
        widgets = {
            'date': DateInput(),
             'amount': TextInput(),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
