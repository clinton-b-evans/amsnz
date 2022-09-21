from django.db import models
from django.utils.timezone import now

# Create your models here.
class Commodity(models.Model):
    class Meta:
        verbose_name_plural = "commodities"
    commodity_class = models.CharField(max_length=120, unique=True)
    spot_price = models.DecimalField(max_digits=6, decimal_places=2, blank = True, default=0.00)

    def __str__(self):
        return f"{self.commodity_class}"

class Transaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
    )
    commodity = models.ForeignKey(Commodity(), on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank = True, default=0.00)
    value = models.DecimalField(max_digits=6, decimal_places=2, blank = True, default=0.00)
    date = models.DateField(null=True, blank=True, default=now)
    
    def __str__(self):
        return f"{self.commodity} - {self.transaction_type}"