from django.core.exceptions import ValidationError
from django.forms import ModelForm

from properties.models import Property
from .models import Reminder
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        fields = ("property",
                  "detail",
                  "due_date",
                  "reminder_type")
        widgets = {
            "due_date": DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.instance.id:
            self.is_edit = True
        else:
            self.is_edit = False
        self.fields['property'].queryset = Property.objects.filter(user=self.user)

    def clean_date(self):
        date = self.cleaned_data['due_date']
        if self.is_edit:
            initial_date = self.initial['due_date']
            if date.year != initial_date.year:
                raise ValidationError(f"Year cannot be changed")
        return date
