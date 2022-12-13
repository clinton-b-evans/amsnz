from django.contrib.auth.models import User
from django.db import models
from properties.models import Property
from django.utils.timezone import now


class Reminder(models.Model):
    property = models.ForeignKey(
        Property, blank=True, null=True, on_delete=models.CASCADE
    )
    REMINDER_TYPES = (
        ("oneoff", "One Off"),
        ("weekly", "Weekly"),
        ("bi-weekly", "Bi-Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("quarterly", "Quarterly"),
    )
    detail = models.TextField(max_length=255, blank=False, null=False)
    due_date = models.DateField(null=True, blank=True, default=now)
    reminder_type = models.CharField(
        choices=REMINDER_TYPES, max_length=120, default="oneoff"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property.name} - {self.detail} - Due: {self.due_date}"

class Notification(models.Model):
    reminder = models.ForeignKey(
        Reminder, on_delete=models.CASCADE
    )
    mark_read = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

