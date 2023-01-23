from django.contrib import admin
from .models import ContactUs

# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
    list_display = ["name", "email", "subject", "message"]
    search_fields = ["name", "email", "subject", "message"]
admin.site.register(ContactUs, ContactUsAdmin)
