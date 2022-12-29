from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from stock_portfolios.models import YEAR_CHOICES


class CrudUser(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)


class CryptoTicker(models.Model):
    name = models.CharField(
        max_length=50,
    )
    ticker = models.CharField(
        max_length=50,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.ticker})"

    class Meta:
        unique_together = (('ticker', 'user'),)


class Crypto(models.Model):
    crypto_ticker = models.ForeignKey(CryptoTicker, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    investment = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    year = models.CharField(choices=YEAR_CHOICES, null=False, blank=False, max_length=4)

    class Meta:
        unique_together = ('user', 'crypto_ticker')

    def __str__(self):
        return f"{self.crypto_ticker}"


class CryptoTransaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    crypto_ticker = models.ForeignKey(CryptoTicker, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=True, blank=True
    )
    quantity = models.FloatField(
        blank=False, default=0.0,
    )
    spot_price = models.FloatField(
        blank=True, default=0.0,
    )
    date = models.DateField(null=True, blank=True, default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.crypto_ticker} - {self.transaction_type}"
