from django.forms import ModelForm
from .models import CashFlow
from django import forms


class CashFlowForm(ModelForm):
    class Meta:
        model = CashFlow
        fields = "__all__"
