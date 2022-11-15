from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_view
from django.contrib.auth import views as auth
urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', include('user.urls')),
    # path('login/', user_view.Login, name ='login'),
    # path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
    # path('register/', user_view.register, name ='register'),
    path("", include("properties.urls", namespace="properties")),
    path("", include("Authentication.urls", namespace="Authentication")),
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
    path(
        "",
        include(
            "stock_portfolios.urls", namespace="stock_portfolios"
        ),
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
