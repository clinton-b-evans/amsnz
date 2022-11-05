from django.db import models
from django.utils.timezone import now

COMMODITY_CLASS_CHOICES = (
    ('ES=F', 'ES=F'),
    ('YM=F', 'YM=F'),
    ('NQ=F', 'NQ=F'),
    ('RTY=F', 'RTY=F'),
    ('ZB=F', 'ZB=F'),
    ('ZN=F', 'ZN=F'),
    ('ZF=F', 'ZF=F'),
    ('ZT=F', 'ZT=F'),
    ('GC=F', 'GC=F'),
    ('MGC=F', 'MGC=F'),
    ('SI=F', 'SI=F'),
    ('SIL=F', 'SIL=F'),
    ('PL=F', 'PL=F'),
    ('HG=F', 'HG=F'),
    ('PA=F', 'PA=F'),
    ('CL=F', 'CL=F'),
    ('HO=F', 'HO=F'),
    ('NG=F', 'NG=F'),
    ('RB=F', 'RB=F'),
    ('BZ=F', 'BZ=F'),
    ('B0=F', 'B0=F'),
    ('ZC=F', 'ZC=F'),
    ('ZO=F', 'ZO=F'),
    ('KE=F', 'KE=F'),
    ('ZR=F', 'ZR=F'),
    ('ZM=F', 'ZM=F'),
    ('ZL=F', 'ZL=F'),
    ('ZS=F', 'ZS=F'),
    ('GF=F', 'GF=F'),
    ('HE=F', 'HE=F'),
    ('LE=F', 'LE=F'),
    ('CC=F', 'CC=F'),
    ('KC=F', 'KC=F'),
    ('CT=F', 'CT=F'),
    ('LBS=F', 'LBS=F'),
    ('OJ=F', 'OJ=F'),
    ('SB=F', 'SB=F'),
)

class Commodity(models.Model):
    commodity_class = models.CharField(
        max_length=50, choices=COMMODITY_CLASS_CHOICES, unique=True
    )
    spot_price = models.DecimalField(
        blank=True, default=0.0, max_digits=8, decimal_places=2
    )
    date = models.DateField(null=True, blank=True, default=now)

    def __str__(self):
        return f"{self.commodity_class}"

    class Meta:
        verbose_name_plural = "commodities"


class Transaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    commodity = models.CharField(
        max_length=50, choices=COMMODITY_CLASS_CHOICES)
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
