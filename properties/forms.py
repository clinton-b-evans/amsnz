from django.forms import ModelForm
from .models import Property
from django import forms
from django.forms import TextInput



class DateInput(forms.DateInput):
    input_type = 'date'

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'purchase_date': DateInput(),
            'land_size': TextInput(),
            'building_size': TextInput(),
            'lounge': TextInput(),
            'bedrooms': TextInput(),
            'bathrooms': TextInput(),
            'parking': TextInput(),
            'vacancy_rate': TextInput(),
            'market_value': TextInput(),
            'purchase_price': TextInput(),
            'deposit': TextInput(),
            'loan_amount': TextInput(),
            'loan_term': TextInput(),
            'interest_rate': TextInput(),
            'repayments': TextInput(),
            'rates': TextInput(),
            'rent': TextInput(),
            'other_income': TextInput(),
            'bodycorp_fee': TextInput(),
            'management_fee': TextInput(),
            'insurance': TextInput(),
            'maintenance': TextInput(),

        }

