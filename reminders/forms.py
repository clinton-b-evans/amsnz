from django.forms import ModelForm
from .models import Reminder
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {
            'due_date': DateInput(),
        }