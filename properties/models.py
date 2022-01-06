from django.db import models

# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=120)
    property_type = models.CharField(max_length=120)
    land_size = models.DecimalField(max_digits=12,decimal_places=2)
    building_size = models.IntegerField(max_length=6)
    bedrooms = models.DecimalField(max_digits=3, decimal_places=2)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=2)
    garage = models.DecimalField(max_digits=3, decimal_places=2)
    vacancy_rate = models.DecimalField(max_digits=3, decimal_places=2)
    street_address = models.TextField()
    purchase_date = models.DateTimeField()
    market_value = models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_term = models.DecimalField(max_digits=3, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=3, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    repayments = models.DecimalField(max_digits=10, decimal_places=2)
    rates = models.DecimalField(max_digits=3, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    other_income = models.DecimalField(max_digits=10, decimal_places=2)
    management_fee = models.DecimalField(max_digits=3, decimal_places=2)
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance  = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (self.name)