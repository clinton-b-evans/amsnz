from django.contrib import admin
from .models import Reminder, Notification

# Register your models here.

admin.site.register(Reminder)
admin.site.register(Notification)