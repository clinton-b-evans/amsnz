from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import PropertyIncomeStatement, PropertyCategory
from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = "date"


class PropertyIncomeStatementForm(ModelForm):
    class Meta:
        model = PropertyIncomeStatement
        fields = ("date",
                  "property",
                  "name",
                  "propcategory",
                  "amount")
        widgets = {
            "date": DateInput(),
            "amount": TextInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(PropertyIncomeStatementForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.instance.id:
            self.is_edit = True
        else:
            self.is_edit = False

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError(f"amount cannot be 0 or negative")
        return amount

    def clean_date(self):
        date = self.cleaned_data['date']
        if self.is_edit:
            initial_date = self.initial['date']
            if date.year != initial_date.year:
                raise ValidationError(f"Year cannot be changed")
        return date


class PropertyCategoryForm(ModelForm):
    class Meta:
        model = PropertyCategory
        fields = "__all__"
