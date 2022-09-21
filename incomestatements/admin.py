from django.contrib import admin
from .models import IncomeStatement, Category

# Register your models here.
admin.site.register(IncomeStatement)
admin.site.register(Category)
