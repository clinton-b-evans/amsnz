from django.contrib.auth.models import User
from django.db import models
from properties.models import Property
from django.utils.timezone import now


# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    occupation = models.CharField(max_length=120, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    service_area = models.CharField(max_length=100, blank=True)
    website_url = models.CharField(max_length=120, null=True, blank=True)
    notes = models.TextField(max_length=300, null=True, blank=True)
    properties = models.ManyToManyField(
        Property,
        blank=True,
        verbose_name="Properties - Hold CTRL/CMD to select multiple",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name}"
