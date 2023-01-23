from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class CashFlow(models.Model):
    description = models.CharField(max_length=200)
    ENTRY_TYPE_SOURCE = (("Income", "Income"), ("Expense", "Expense"))
    FREQUENCY_TYPE_SOURCE = (
        ("Weekly", "Weekly"),
        ("Fortnightly", "Fortnightly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    )
    entry_type = models.CharField(
        choices=ENTRY_TYPE_SOURCE,
        max_length=100,
        null=False,
        blank=False,
        default="Expense",
    )
    frequency = models.CharField(
        choices=FREQUENCY_TYPE_SOURCE,
        max_length=100,
        null=False,
        blank=False,
        default="Monthly",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True, default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.entry_type} - {self.amount}"
