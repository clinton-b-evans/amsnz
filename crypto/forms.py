from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Crypto, CryptoTransaction
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class CryptoForm(ModelForm):
    class Meta:
        model = Crypto
        fields = ("name", "ticker", "quantity")
class TransactionForm(ModelForm):
    class Meta:
        model = CryptoTransaction
        fields = "__all__"
        widgets = {
            "date": DateInput(),
        }

    def clean_quantity(self):
        transaction_type = self.data['transaction_type']
        coin = self.cleaned_data['coin']
        quantity = self.cleaned_data['quantity']
        if transaction_type == 'Sell':
            if coin.quantity - float(quantity) < 0:
                raise ValidationError("You don't have sufficient quantity")
        return quantity