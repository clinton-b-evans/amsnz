from django.db import models
from incomestatements.models import Category


class Budget(models.Model):
    budget_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.CharField(null=False, blank=False, max_length=4)
    january_budget = models.FloatField(null=True, blank=True, default=0)
    february_budget = models.FloatField(null=True, blank=True, default=0)
    march_budget = models.FloatField(null=True, blank=True, default=0)
    april_budget = models.FloatField(null=True, blank=True, default=0)
    may_budget = models.FloatField(null=True, blank=True, default=0)
    june_budget = models.FloatField(null=True, blank=True, default=0)
    july_budget = models.FloatField(null=True, blank=True, default=0)
    august_budget = models.FloatField(null=True, blank=True, default=0)
    september_budget = models.FloatField(null=True, blank=True, default=0)
    october_budget = models.FloatField(null=True, blank=True, default=0)
    november_budget = models.FloatField(null=True, blank=True, default=0)
    december_budget = models.FloatField(null=True, blank=True, default=0)

