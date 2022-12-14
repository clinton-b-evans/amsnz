import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Crypto, CryptoTransaction, CryptoTicker
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class CryptoForm(ModelForm):
    class Meta:
        model = Crypto
        fields = ("crypto_ticker", "quantity")


class CryptoTickerForm(ModelForm):
    class Meta:
        model = CryptoTicker
        fields = ("name", "ticker")

    def __init__(self, user, *args, **kwargs):
        super(CryptoTickerForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_ticker(self):
        ticker = self.cleaned_data["ticker"]
        try:
            CryptoTicker.objects.get(ticker=ticker, user=self.user)
        except CryptoTicker.DoesNotExist:
            pass
        else:
            raise ValidationError('Ticker with this Name already exists.')
        # Always return cleaned_data
        return ticker


class TransactionForm(ModelForm):
    class Meta:
        model = CryptoTransaction
        fields = ("crypto_ticker",
                  "transaction_type",
                  "spot_price",
                  "quantity",
                  "date")
        widgets = {
            "date": DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.instance.id:
            self.is_edit = True
        else:
            self.is_edit = False

    def clean_quantity(self):
        if self.is_edit is True:
            initial_quantity = self.initial['quantity']
            initial_spot_price = self.initial['spot_price']
            initial_transaction_type = self.initial['transaction_type']
            initial_date = self.initial['date']
        else:
            self.is_edit = False
        transaction_type = self.data['transaction_type']
        crypto_ticker = self.cleaned_data['crypto_ticker']
        quantity = self.cleaned_data['quantity']
        spot_price = float(self.data['spot_price'])
        date = self.data['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        crypto, created = Crypto.objects.get_or_create(crypto_ticker=crypto_ticker,
                                                       user=self.user,
                                                       year=str(date.year))
        if self.is_edit is False:
            if quantity <= 0:
                raise ValidationError(f"Quantity cannot be 0 or negative")
            if transaction_type == 'Sell':
                if crypto.quantity - float(quantity) < 0:
                    raise ValidationError(f"You cannot sell more than {crypto.quantity}")

            if transaction_type == 'Buy':
                crypto.quantity += quantity
                crypto.investment += quantity * spot_price
                crypto.save()
            else:
                if crypto.quantity - quantity > -1:
                    crypto.quantity -= quantity
                    if crypto.investment - quantity * spot_price < 0:
                        crypto.investment = float(0.0)
                    else:
                        crypto.investment -= quantity * spot_price
                    crypto.save()
                else:
                    raise ValidationError("You don't have sufficient quantity")
            return quantity
        else:
            if transaction_type == 'Buy':
                # if spot_price changed
                if "spot_price" in self.changed_data:
                    if "quantity" in self.changed_data:
                        crypto.quantity -= initial_quantity
                        crypto.quantity += quantity
                        crypto.investment -= initial_quantity * initial_spot_price
                        crypto.investment += quantity * spot_price
                        crypto.save()
                    else:
                        crypto.investment -= quantity * initial_spot_price
                        crypto.investment += quantity * spot_price
                        crypto.save()
                # if quantity changed and spotPrice didn't change
                if initial_quantity != quantity and initial_spot_price == spot_price:
                    crypto.quantity -= initial_quantity
                    crypto.quantity += quantity
                    crypto.investment -= initial_quantity * spot_price
                    crypto.investment += quantity * spot_price
                    crypto.save()
            # when transactions_type is sell
            else:
                # if spot_price changed
                if "spot_price" in self.changed_data:
                    # if quantity changed
                    if initial_quantity != quantity:
                        crypto.quantity -= initial_quantity
                        crypto.quantity += quantity
                        crypto.investment += initial_quantity * spot_price
                        crypto.investment -= quantity * spot_price
                    else:
                        crypto.investment += initial_quantity * spot_price
                        crypto.investment -= quantity * spot_price
                    crypto.save()
                # if quantity changed and spotPrice didn't change
                if initial_quantity != quantity and initial_spot_price == spot_price:
                    crypto.quantity -= quantity
                    crypto.quantity += initial_quantity
                    crypto.investment += quantity * spot_price
                    crypto.investment -= initial_quantity * spot_price
                    crypto.save()
            return quantity

    def clean_spot_price(self):
        spot_price = self.cleaned_data['spot_price']
        if spot_price <= 0:
            raise ValidationError(f"Spot price cannot be 0 or negative")
        return spot_price

    def clean_transaction_type(self):
        transaction_type = self.cleaned_data['transaction_type']
        if "transaction_type" in self.changed_data and self.instance.id:
            raise ValidationError(f"Transaction type cannot be changed")
        return transaction_type

    def clean_date(self):
        date = self.cleaned_data['date']
        if self.is_edit:
            initial_date = self.initial['date']
            if date.year != initial_date.year:
                raise ValidationError(f"Year cannot be changed")
        return date
