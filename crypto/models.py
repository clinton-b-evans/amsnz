from django.db import models
from django.utils.timezone import now


class Crypto(models.Model):
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
    quantity = models.FloatField(
        blank=False, default=0.0,
    )
    spot_price = models.FloatField(
        blank=True, default=0.0,
    )
    date = models.DateField(null=True, blank=True, default=now)

    def __str__(self):
        return f"{self.coin} - {self.transaction_type}"
