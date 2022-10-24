from django.urls import path
from .views import (
    commodity_list_view,
    commodity_detail_view,
    add_commodity,
    update_commodity,
    delete_commodity,
    add_transaction,
    update_transaction,
    delete_transaction,
)

app_name = "commodities"

urlpatterns = [
    path("commodities/<str:year>/", commodity_list_view, name="commodities_list"),
    path("commodities/add", add_commodity, name="add"),
    path(
        "commodities/transaction/add/<str:pk>", add_transaction, name="transaction-add"
    ),
    path("commodities/<pk>/", commodity_detail_view, name="detail"),
    path("commodities/<str:pk>/edit", update_commodity, name="update"),
    path(
        "commodities/transaction/<str:pk>/edit",
        update_transaction,
        name="update-transaction",
    ),
    path("commodities/<str:pk>/delete", delete_commodity, name="delete"),
    path(
        "commodities/transaction/<str:pk>/delete",
        delete_transaction,
        name="delete-transaction",
    ),
]
