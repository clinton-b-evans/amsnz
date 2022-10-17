from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("properties.urls", namespace="properties")),
    path("", include("reminders.urls", namespace="reminders")),
    path("", include("contacts.urls", namespace="contacts")),
    path("", include("personal_balances.urls", namespace="personalbalance")),
    path("", include("market_funds.urls", namespace="marketfunds")),
    path("", include("cash_flows.urls", namespace="cashflows")),
    path("", include("commodities.urls", namespace="commodities")),
    path("", include("retirement_goals.urls", namespace="retirement")),
    path("", include("crypto.urls", namespace="crypto")),
    path("", include("incomestatements.urls", namespace="incomestatements")),
    path(
        "",
        include(
            "incomestatements_property.urls", namespace="property-incomestatements"
        ),
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
