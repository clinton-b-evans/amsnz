from django.forms import ModelForm
from .models import IndexFund, Trade
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class IndexFundForm(ModelForm):
    class Meta:
        model = IndexFund
        fields = "__all__"


class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = "__all__"
        widgets = {
            "date": DateInput(),
        }
