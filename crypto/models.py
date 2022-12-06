from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class CrudUser(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)


class Crypto(models.Model):
    name = models.CharField(
        max_length=50,
    )
    ticker = models.CharField(
        max_length=50,
    )
    quantity = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    investment = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    year = models.CharField(null=False, blank=False, max_length=4)


    class Meta:
        unique_together = ('user', 'ticker', 'name')

    def __str__(self):
        return f"{self.name}"


class CryptoTransaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    coin = models.ForeignKey(Crypto, on_delete=models.CASCADE, null=True, blank=True)
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
        return f"{self.coin} - {self.transaction_type}"
