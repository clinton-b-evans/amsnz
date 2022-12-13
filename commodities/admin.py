from django.contrib import admin
from .models import Commodity, Transaction, CommodityClass

# Register your models here.

admin.site.register(Commodity)
admin.site.register(Transaction)
admin.site.register(CommodityClass)
