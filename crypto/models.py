from django.db import models

# Create your models here.
class Crypto(models.Model):
    
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=6, null = True, blank = True)
    qty = models.DecimalField(max_digits=12, decimal_places=4, blank = True, default=0.00)
    spot_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0.00)

    def __str__(self):
        if self.ticker is None:
            return f"{self.name}"
        else:
            return f"{self.ticker } - {self.name}"