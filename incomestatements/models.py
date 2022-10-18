from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=120)
    TRANSACTION_TYPE_SOURCES = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"


class IncomeStatement(models.Model):
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=True
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, default=0.00
    )

    def __str__(self):
        return f"{self.name}"
