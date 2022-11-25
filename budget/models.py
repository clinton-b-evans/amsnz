from django.db import models
from incomestatements.models import Category


class Budget(models.Model):
    self = models.ForeignKey(Category, on_delete=models.CASCADE)
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
    def compute_budget(self):
        return self.january_budget + self.february_budget + self.march_budget + self.april_budget + self.may_budget + self.june_budget + self.july_budget + self.august_budget + self.september_budget + self.october_budget + self.november_budget + self.december_budget

