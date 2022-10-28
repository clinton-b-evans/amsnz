from django.db import models
from django.utils.timezone import now


class IndexFund(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=6, null=True, blank=True)
    asset_class = models.CharField(max_length=30)
    date = models.DateField(null=True, blank=True, default=now)
    ASSET_CLASS_SOURCES = (
        ("Equities", "Equities"),
        ("Bonds", "Bonds"),
        ("Cash & Cash Equivalents", "Cash & Cash Equivalents"),
        ("Commodites", "Commodites"),
        ("Diversified", "Diversified"),
        ("Reits", "Reits"),
        ("Other", "Other"),
    )
    asset_class = models.CharField(
        choices=ASSET_CLASS_SOURCES, max_length=100, null=True, blank=True
    )
    FUND_TYPE_SOURCES = (
        ("Index Fund", "Index Fund"),
        ("Exchange Traded Fund", "Exchange Traded Fund"),
    )
    fund_type = models.CharField(
        choices=FUND_TYPE_SOURCES, max_length=100, null=True, blank=False
    )
    shares = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, default=0.00
    )
    share_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, default=0.00
    )

    def __str__(self):
        if self.ticker is None:
            return f"{self.name}"
        else:
            return f"{self.ticker } - {self.name}"


class Trade(models.Model):
    date = models.DateField()
    indexfund = models.ForeignKey(
        IndexFund, on_delete=models.CASCADE, blank=True, null=True
    )
    TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    type = models.CharField(
        choices=TYPE_SOURCES, max_length=100, null=True, blank=False
    )

    shares = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, default=0.00
    )
    share_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, default=0.00
    )

    def __str__(self):
        return f"{self.date} - {self.indexfund } -- ({self.type})"
