from django.contrib import admin

from .models import PropertyIncomeStatement, PropertyCategory


class PropertyIncomeStatementAdmin(admin.ModelAdmin):
    model = PropertyIncomeStatement
    list_display = ["name", "propcategory", "property", "date", "amount"]
    search_fields = ["name", "propcategory", "property", "date", "amount"]


# Register your models here.
admin.site.register(PropertyIncomeStatement, PropertyIncomeStatementAdmin)
admin.site.register(PropertyCategory)

# Register your models here.
