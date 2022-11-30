from django.contrib.auth.models import User
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
    year = models.CharField(null=False, blank=False, max_length=4)
    january_budget = models.FloatField(null=True, blank=True, default=0)
    february_budget = models.FloatField(null=True, blank=True, default=0)
    march_budget = models.FloatField(null=True, blank=True, default=0)
    april_budget = models.FloatField(null=True, blank=True, default=0)
    may_budget = models.FloatField(null=True, blank=True, default=0)
    june_budget = models.FloatField(null=True, blank=True, default=0)
    july_budget = models.FloatField(null=True, blank=True, default=0)
    august_budget = models.FloatField(null=True, blank=True, default=0)
    september_budget = models.FloatField(null=True, blank=True, default=0)
    october_budget = models.FloatField(null=True, blank=True, default=0)
    november_budget = models.FloatField(null=True, blank=True, default=0)
    december_budget = models.FloatField(null=True, blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def months_data(self):
        data = {
            "January": self.january_budget,
            "February": self.february_budget,
            "March": self.march_budget,
            "April": self.april_budget,
            "May": self.may_budget,
            "June": self.june_budget,
            "July": self.july_budget,
            "August": self.august_budget,
            "September": self.september_budget,
            "October": self.october_budget,
            "November": self.november_budget,
            "December": self.december_budget,
        }
        return data
    def compute_budget(self):
        return self.january_budget + self.february_budget + self.march_budget + self.april_budget + self.may_budget + self.june_budget + self.july_budget + self.august_budget + self.september_budget + self.october_budget + self.november_budget + self.december_budget

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"
