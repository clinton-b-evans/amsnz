from django.contrib import admin
from .models import Stock, StockTransaction

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockTransaction)
