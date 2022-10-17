from django.forms import ModelForm
from .models import PropertyIncomeStatement, PropertyCategory
from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = "date"


class PropertyIncomeStatementForm(ModelForm):
    class Meta:
        model = PropertyIncomeStatement
        fields = "__all__"
        widgets = {
            "date": DateInput(),
            "amount": TextInput(),
        }


class PropertyCategoryForm(ModelForm):
    class Meta:
        model = PropertyCategory
        fields = "__all__"
