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
        max_length=50, choices=COMMODITY_NAME_CHOICES, unique=True
    )
    commodity_class = models.CharField(
        max_length=50, choices=COMMODITY_CLASS_CHOICES, unique=True
    )
    weight = models.DecimalField(
        null=False, blank=False, default=0.0, max_digits=8, decimal_places=2
    )
    investment = models.DecimalField(
        null=False, blank=False, default=0.0, max_digits=8, decimal_places=2
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "commodities"


class Transaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False
    )
    weight = models.DecimalField(
        blank=True, default=0.0, max_digits=8, decimal_places=2
    )
    value = models.DecimalField(blank=True, default=0.0, max_digits=8, decimal_places=4)
    date = models.DateField(null=True, blank=True, default=now)

    def __str__(self):
        return f"{self.commodity} - {self.transaction_type}"
