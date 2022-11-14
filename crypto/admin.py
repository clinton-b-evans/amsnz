from django.contrib import admin
from .models import Crypto, CryptoTransaction, CrudUser

# Register your models here.
admin.site.register(Crypto)
admin.site.register(CryptoTransaction)
admin.site.register(CrudUser)