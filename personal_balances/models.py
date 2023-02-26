from django.contrib.auth.models import User
from django.db import models
from properties.models import Property
from django.utils.timezone import now


# Create your models here.


class PersonalBalance(models.Model):
    description = models.CharField(max_length=200)
    ENTRY_TYPE_SOURCE = (
        ("Asset", "Asset"),
        ("Liability", "Liability"),
        ("Savings", "Savings"),
        ("Retirement Acc", "Retirement Acc"),
    )
    entry_type = models.CharField(
        choices=ENTRY_TYPE_SOURCE, max_length=100, null=False, blank=False
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.entry_type} - {self.amount}"
