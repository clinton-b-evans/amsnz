from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from datetime import datetime
from django.utils.timezone import now


class Property(models.Model):
    name = models.CharField(max_length=120)

    PROPERTY_TYPE_SOURCES = (
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
        ("Industrial", "Industrial"),
        ("Retail", "Retail"),
        ("Land", "Land"),
        ("Other", "Other"),
    )
    property_type = models.CharField(
        choices=PROPERTY_TYPE_SOURCES, max_length=100, null=True, blank=True
    )
    land_size = models.PositiveIntegerField(null=True, blank=True, default=0)
    building_size = models.PositiveIntegerField(default=0)
    lounge = models.PositiveIntegerField(default=0)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    parking = models.PositiveIntegerField(default=0)

    GARAGE_SOURCES = (
        ("None", "None"),
        ("Carport", "Carport"),
        ("Single", "Single"),
        ("Single with Workshop", "Single with Workshop"),
        ("Double", "Double"),
        ("Double with Workshop", "Double with Workshop"),
        ("Other", "Other"),
    )
    garage = models.CharField(
        choices=GARAGE_SOURCES, max_length=100, null=True, blank=True
    )
    vacancy_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="Vacancy Rate %"
    )
    street_address = models.TextField(null=True, blank=True)

    purchase_date = models.DateField(null=True, blank=True, default=now)
    market_value = models.PositiveIntegerField(default=1000)
    purchase_price = models.PositiveIntegerField(default=0)
    deposit = models.PositiveIntegerField(default=0)
    loan_amount = models.PositiveIntegerField(default=0)
    loan_term = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Interest Rate %"
    )
    repayments = models.DecimalField(max_digits=10, decimal_places=2)
    rates = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=12, decimal_places=2)
    other_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, default=0.00
    )
    bodycorp_fee = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, default=0.00
    )
    management_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        default=0.00,
        verbose_name="Management fee %",
    )
    insurance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, default=0.00
    )
    maintenance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, default=0.00
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)

    image = models.ImageField(upload_to="products", default="no_picture.png")

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"pk": self.pk})


class Transactions(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    TRANSACTION_TYPES = (
        ("expense", "Expense"),
        ("income", "Income"),
    )

    CATEGORY_TYPES = (
        ("Capital Introduced", "Capital Introduced"),
        ("Management Fee", "Management Fee"),
        ("Insurance", "Insurance"),
        ("Interest", "Interest"),
        ("Mortage", "Mortage"),
        ("Repairs and Maintenance", "Repairs and Maintenance"),
        ("Rates", "Rates"),
        ("Rent Received", "Rent Received"),
        ("Sundry Expense", "Sundry Expense"),
        ("Other", "Other"),
    )

    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=120)
    comments = models.TextField(max_length=255, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_TYPES, max_length=128)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.property_id.name} {self.transaction_type}: ${self.amount} for {self.category}"
