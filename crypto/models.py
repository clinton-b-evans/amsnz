from django.db import models
from django.utils.timezone import now

class Crypto(models.Model):
    name = models.CharField(
        max_length=50, unique=True
    )
    ticker = models.CharField(
        max_length=50, unique=True
    )
    quantity = models.DecimalField(
        null=False, blank=False, default=0.0, max_digits=8, decimal_places=2
    )
    total_investment = models.DecimalField(
        null=False, blank=False, default=0.0, max_digits=8, decimal_places=2
    )
    def __str__(self):
        return f"{self.name}"
class CryptoTransaction(models.Model):

    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    coin = models.ForeignKey(Crypto, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False
    )
    quantity = models.DecimalField(
        blank=False, default=0.0, max_digits=8, decimal_places=2
    )
    spot_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, default=0.0
    )
    date = models.DateField(null=True, blank=True, default=now)

    def __str__(self):
        return f"{self.coin} - {self.transaction_type}"