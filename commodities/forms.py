from django.forms import ModelForm
from .models import Commodity, Transaction
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class CommodityForm(ModelForm):
    class Meta:
        model = Commodity
        fields = '__all__'

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }