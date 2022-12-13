import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Commodity, Transaction, CommodityClass
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class CommodityClassForm(ModelForm):
    class Meta:
        model = CommodityClass
        fields = ("name", "commodity_class")

    def __init__(self, user, *args, **kwargs):
        super(CommodityClassForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_ticker(self):
        commodity_class = self.cleaned_data["commodity_class"]
        try:
            CommodityClass.objects.get(commodity_class=commodity_class, user=self.user)
        except CommodityClass.DoesNotExist:
            pass
        else:
            raise ValidationError('Commodity Class with this Name already exists.')
        # Always return cleaned_data
        return commodity_class


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ("commodity",
                  "transaction_type",
                  "value",
                  "weight",
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

    def clean_weight(self):
        if self.is_edit is True:
            initial_weight = self.initial['weight']
            initial_value = self.initial['value']
            initial_transaction_type = self.initial['transaction_type']
            initial_date = self.initial['date']
        else:
            self.is_edit = False
        transaction_type = self.data['transaction_type']
        commodity = self.cleaned_data['commodity']
        weight = self.cleaned_data['weight']
        value = float(self.data['value'])
        date = self.data['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        commodity, created = Commodity.objects.get_or_create(commodity_class=commodity,
                                                             user=self.user,
                                                             year=str(date.year))
        if self.is_edit is False:
            if weight <= 0:
                raise ValidationError(f"Quantity cannot be 0 or negative")
            if transaction_type == 'Sell':
                if commodity.weight - float(weight) < 0:
                    raise ValidationError(f"You cannot sell more than {commodity.weight}")

            if transaction_type == 'Buy':
                commodity.weight += weight
                commodity.investment += weight * value
                commodity.save()
            else:
                if commodity.weight - weight > -1:
                    commodity.weight -= weight
                    if commodity.investment - weight * value < 0:
                        commodity.investment = float(0.0)
                    else:
                        commodity.investment -= weight * value
                    commodity.save()
                else:
                    raise ValidationError("You don't have sufficient weight")
            return weight
        else:
            if transaction_type == 'Buy':
                # if value changed
                if "value" in self.changed_data:
                    if "weight" in self.changed_data:
                        commodity.weight -= initial_weight
                        commodity.weight += weight
                        commodity.investment -= initial_weight * initial_value
                        commodity.investment += weight * value
                        commodity.save()
                    else:
                        commodity.investment -= weight * initial_value
                        commodity.investment += weight * value
                        commodity.save()
                # if weight changed and spotPrice didn't change
                if initial_weight != weight and initial_value == value:
                    commodity.weight -= initial_weight
                    commodity.weight += weight
                    commodity.investment -= initial_weight * value
                    commodity.investment += weight * value
                    commodity.save()
            # when transactions_type is sell
            else:
                # if value changed
                if "value" in self.changed_data:
                    # if weight changed
                    if initial_weight != weight:
                        commodity.weight -= initial_weight
                        commodity.weight += weight
                        commodity.investment += initial_weight * value
                        commodity.investment -= weight * value
                    else:
                        commodity.investment += initial_weight * value
                        commodity.investment -= weight * value
                    commodity.save()
                # if weight changed and spotPrice didn't change
                if initial_weight != weight and initial_value == value:
                    commodity.weight -= weight
                    commodity.weight += initial_weight
                    commodity.investment += weight * value
                    commodity.investment -= initial_weight * value
                    commodity.save()
            return weight

    def clean_value(self):
        value = self.cleaned_data['value']
        if value <= 0:
            raise ValidationError(f"Value cannot be 0 or negative")
        return value

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
