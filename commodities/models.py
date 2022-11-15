from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

COMMODITY_CLASS_CHOICES = (
    ('GC=F', 'GC=F'),
    ('SI=F', 'SI=F'),
    ('PL=F', 'PL=F'),
    ("PA=F", "PA=F")
)

COMMODITY_NAME_CHOICES = (
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
    ('Platinum', 'Platinum'),
    ("Palladium", "Palladium")
)


class Commodity(models.Model):
    name = models.CharField(
        max_length=50, choices=COMMODITY_NAME_CHOICES,
    )
    commodity_class = models.CharField(
        max_length=50, choices=COMMODITY_CLASS_CHOICES,
    )
    weight = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    investment = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'commodity_class', 'name')
        verbose_name_plural = "commodities"

    def __str__(self):
        return f"{self.name}"



class Transaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False
    )
    weight = models.FloatField(
        blank=True, default=0.0,
    )
    value = models.FloatField(blank=True, default=0.0, )
    date = models.DateField(null=True, blank=True, default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.commodity} - {self.transaction_type}"
