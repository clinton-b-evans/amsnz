from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Stock, StockTransaction
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ("name", "ticker", "quantity")
class TransactionForm(ModelForm):
    class Meta:
        model = StockTransaction
        fields = "__all__"
        widgets = {
            "date": DateInput(),
        }

    def clean_quantity(self):
        transaction_type = self.data['transaction_type']
        stock = self.cleaned_data['stock']
        quantity = self.cleaned_data['quantity']
        if transaction_type == 'Sell':
            if stock.quantity - float(quantity) < 0:
                raise ValidationError("You don't have sufficient quantity")
        return quantity