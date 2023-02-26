from django.core.exceptions import ValidationError
from django.forms import ModelForm

from properties.models import Property
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

    def __init__(self, user,year, *args, **kwargs):
        super(PropertyIncomeStatementForm, self).__init__(*args, **kwargs)
        self.user = user
        self.year = year
        if self.instance.id:
            self.is_edit = True
        else:
            self.is_edit = False
        self.fields['property'].queryset = Property.objects.filter(user=self.user)
        self.fields['propcategory'].queryset = PropertyCategory.objects.filter(user=self.user)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError(f"amount cannot be 0 or negative")
        return amount

    def clean_date(self):
        print(self.data,'data')
        date = self.cleaned_data['date']
        category_id = self.data['propcategory']
        category = PropertyCategory.objects.get(id=category_id)
        if self.is_edit:
            initial_date = self.initial['date']
            if date.year != initial_date.year:
                raise ValidationError(f"Year cannot be changed")
        else:
            if int(category.year) != date.year:
                raise ValidationError(f"Budget against this Category does not exist in this year, Please add first!")
        return date


class PropertyCategoryForm(ModelForm):
    class Meta:
        model = PropertyCategory
        fields = "__all__"
