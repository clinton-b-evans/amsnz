import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Stock, StockTransaction, StockTicker
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ("stock_ticker", "year", "quantity")


class StockTickerForm(ModelForm):
    class Meta:
        model = StockTicker
        fields = ("name", "ticker", "stock_type", "stock_category")

    def __init__(self, user, *args, **kwargs):
        super(StockTickerForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_ticker(self):
        ticker = self.cleaned_data["ticker"]
        try:
            StockTicker.objects.get(ticker=ticker, user=self.user)
        except StockTicker.DoesNotExist:
            pass
        else:
            raise ValidationError('Ticker with this Name already exists.')
        # Always return cleaned_data
        return ticker

class TransactionForm(ModelForm):
    class Meta:
        model = StockTransaction
        fields = ("stock_ticker",
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
        self.fields['stock_ticker'].queryset = StockTicker.objects.filter(user=self.user)

    def clean_quantity(self):
        if self.is_edit is True:
            initial_quantity = self.initial['quantity']
            initial_spot_price = self.initial['spot_price']
            initial_transaction_type = self.initial['transaction_type']
            initial_date = self.initial['date']
        else:
            self.is_edit = False
        transaction_type = self.data['transaction_type']
        stock_ticker = self.cleaned_data['stock_ticker']
        quantity = self.cleaned_data['quantity']
        spot_price = float(self.data['spot_price'])
        date = self.data['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        stock, created = Stock.objects.get_or_create(stock_ticker=stock_ticker,
                                                     user=self.user,
                                                     year=str(date.year))
        if self.is_edit is False:
            if quantity <= 0 :
                raise ValidationError(f"Quantity cannot be 0 or negative")
            if transaction_type == 'Sell':
                if stock.quantity - float(quantity) < 0:
                    raise ValidationError(f"You cannot sell more than {stock.quantity}")

            if transaction_type == 'Buy':
                stock.quantity += quantity
                stock.investment += quantity * spot_price
                stock.save()
            else:
                if stock.quantity - quantity > -1:
                    stock.quantity -= quantity
                    if stock.investment - quantity * spot_price < 0:
                        stock.investment = float(0.0)
                    else:
                        stock.investment -= quantity * spot_price
                    stock.save()
                else:
                    raise ValidationError("You don't have sufficient quantity")
            return quantity
        else:
            if transaction_type == 'Buy':
                # if spot_price changed
                if "spot_price" in self.changed_data:
                    if "quantity" in self.changed_data:
                        stock.quantity -= initial_quantity
                        stock.quantity += quantity
                        stock.investment -= initial_quantity * initial_spot_price
                        stock.investment += quantity * spot_price
                        stock.save()
                    else:
                        stock.investment -= quantity * initial_spot_price
                        stock.investment += quantity * spot_price
                        stock.save()
                # if quantity changed and spotPrice didn't change
                if initial_quantity != quantity and initial_spot_price == spot_price:
                    stock.quantity -= initial_quantity
                    stock.quantity += quantity
                    stock.investment -= initial_quantity * spot_price
                    stock.investment += quantity * spot_price
                    stock.save()
            # when transactions_type is sell
            else:
                # if spot_price changed
                if "spot_price" in self.changed_data:
                    # if quantity changed
                    if initial_quantity != quantity:
                        stock.quantity -= initial_quantity
                        stock.quantity += quantity
                        stock.investment += initial_quantity * spot_price
                        stock.investment -= quantity * spot_price
                    else:
                        stock.investment += initial_quantity * spot_price
                        stock.investment -= quantity * spot_price
                    stock.save()
                # if quantity changed and spotPrice didn't change
                if initial_quantity != quantity and initial_spot_price == spot_price:
                    stock.quantity -= quantity
                    stock.quantity += initial_quantity
                    stock.investment += quantity * spot_price
                    stock.investment -= initial_quantity * spot_price
                    stock.save()
            return quantity
    def clean_spot_price(self):
        spot_price = self.cleaned_data['spot_price']
        if spot_price <= 0 :
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
            if date.year != initial_date.year :
                raise ValidationError(f"Year cannot be changed")
        return date