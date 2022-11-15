from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Stock(models.Model):
    name = models.CharField(
        max_length=50, unique=True
    )
    ticker = models.CharField(
        max_length=50, unique=True
    )
    quantity = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    investment = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    def __str__(self):
        return f"{self.name}"
class StockTransaction(models.Model):

    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False
    )
    quantity = models.FloatField(
        blank=False, default=0.0,
    )
    spot_price = models.FloatField(
         blank=True, default=0.0
    )
    date = models.DateField(null=True, blank=True, default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.stock} - {self.transaction_type}"