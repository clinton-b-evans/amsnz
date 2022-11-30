from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class RetirementGoal(models.Model):
    start_date = models.DateField(null=True, blank=True, default=now)
    networth_goal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Networth Goal"
    )
    cpi = models.DecimalField(
        max_digits=4, decimal_places=2, default=0, verbose_name="Consumer Price Index"
    )
    real_estate = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    stocks = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    crypto = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    commodities = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    collectables = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    cash = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    real_estate_swr = models.DecimalField(
        max_digits=4, decimal_places=2, default=0, verbose_name="RE SWR"
    )
    stocks_swr = models.DecimalField(
        max_digits=4, decimal_places=2, default=0, verbose_name="Stocks SWR"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.networth_goal)
