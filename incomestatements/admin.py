from django.contrib import admin
from .models import IncomeStatement, Category, CategoryName

# Register your models here.
admin.site.register(IncomeStatement)
admin.site.register(Category)
admin.site.register(CategoryName)