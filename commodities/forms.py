from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Commodity, Transaction
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class CommodityForm(ModelForm):
    class Meta:
        model = Commodity
        fields = ("commodity_class", "weight")


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        widgets = {
            "date": DateInput(),
        }

    def clean_weight(self):
        transaction_type = self.data['transaction_type']
        commodity = self.cleaned_data['commodity']
        weight = self.cleaned_data['weight']
        if transaction_type == 'Sell':
            if commodity.weight - Decimal(weight) < 0:
                raise ValidationError("You don't have sufficient weight")
        return weight

