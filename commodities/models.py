from django.db import models
from django.utils.timezone import now

COMMODITY_CLASS_CHOICES = (
        ("ROKU", "ROKU"),
        ("GOLD", "GOLD"),
        ("QCOM", "QCOM"),
        ("HOOD", "HOOD"),
        ("ETSY", "ETSY"),
        ("SU", "SU"),
        ("LUMN", "LUMN"),
        ("REGN", "REGN"),
        ("CI", "CI"),
        ("MAR", "MAR"),
        ("APD", "APD"),
        ("SQQQ", "SQQQ"),
        ("FTNT", "FTNT"),
        ("BKNG", "BKNG"),
        ("EBAY", "EBAY"),
        ("MRNA", "MRNA"),
        ("RUN", "RUN"),
        ("GBPUSD=X", "GBPUSD=X"),
        ("NQ=F", "NQ=F"),
        ("COMS", "COMS"),
        ("NFLX", "NFLX"),
        ("HUBS", "HUBS"),
        ("EURUSD=X", "EURUSD=X"),
        ("ARKK", "ARKK"),
        ("MATIC-USD", "MATIC-USD"),
        ("DDOG", "DDOG"),
        ("SPY", "SPY"),
        ("NETC.CO", "NETC.CO"),
        ("TQQQ", "TQQQ"),
        ("BT-A.L", "BT-A.L"),
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
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
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
