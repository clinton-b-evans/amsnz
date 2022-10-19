from django.contrib import admin
from .models import Commodity, Transaction

# Register your models here.

admin.site.register(Commodity)
admin.site.register(Transaction)
