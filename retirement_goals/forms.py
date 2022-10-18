from django.forms import ModelForm
from .models import RetirementGoal
from django import forms
from django.forms.fields import DateField


class DateInput(forms.DateInput):
    input_type = "date"


class RetirementGoalForm(ModelForm):
    class Meta:
        model = RetirementGoal
        fields = "__all__"
        widgets = {
            "real_estate": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "stocks": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "crypto": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "commodities": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "collectables": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "cash": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 3,
                    "onKeyUp": "checkTotal(this.id, this.value)",
                }
            ),
            "real_estate_swr": forms.TextInput(
                attrs={
                    "size": 3,
                    "maxlength": 4,
                    "onKeyUp": "swrUpdate()",
                    "onKeyPress": "numberWithCommas(this.value)",
                }
            ),
            "stocks_swr": forms.TextInput(
                attrs={"size": 3, "maxlength": 4, "onKeyUp": "swrUpdate()"}
            ),
            "networth_goal": forms.TextInput(
                attrs={"size": 11, "onKeyUp": "numbersWithCommas(this.value)"}
            ),
            "cpi": forms.TextInput(attrs={"size": 4}),
            "start_date": DateInput(),
        }
