from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import IncomeStatement, Category, CategoryName
from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = "date"


class IncomeStatementForm(ModelForm):
    class Meta:
        model = IncomeStatement
        fields = ("date",
                  "name",
                  "category",
                  "amount")
        widgets = {
            "date": DateInput(),
            "amount": TextInput(),
        }

    def __init__(self, user, year, *args, **kwargs):
        super(IncomeStatementForm, self).__init__(*args, **kwargs)
        self.user = user
        self.year = year
        if self.instance.id:
            self.is_edit = True
        else:
            self.is_edit = False
        self.fields['category'].queryset = Category.objects.filter(user=self.user)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError(f"amount cannot be 0 or negative")
        return amount

    def clean_date(self):
        date = self.cleaned_data['date']
        category_id = self.data['category']
        category = Category.objects.get(id=category_id)
        if self.is_edit:
            initial_date = self.initial['date']
            if date.year != initial_date.year:
                raise ValidationError(f"Year cannot be changed")
        else:
            if int(category.year) != date.year:
                raise ValidationError(f"Budget against this Category does not exist in this year, Please add first!")
        return date


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
