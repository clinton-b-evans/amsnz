from django.db import models
from properties.models import Property
from django.utils.timezone import now



# Create your models here.

class Reminder(models.Model):
    property = models.ForeignKey(Property, blank=True, null=True, on_delete=models.CASCADE)
    REMINDER_TYPES = (
    ('oneoff', 'One Off'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
    )
    detail = models.TextField(max_length=255, blank=False, null=False)
    due_date = models.DateField(null=True, blank=True, default=now)
    reminder_type = models.CharField(choices=REMINDER_TYPES, max_length=120, default='oneoff')

    def __str__(self):
        return f"{self.property.name} - {self.detail} - Due: {self.due_date}"
