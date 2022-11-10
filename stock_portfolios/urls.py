from django.urls import path
from .views import (
    stock_list_view,
    stock_transactions,
    add_transaction,
    update_transaction,
    delete_transaction, add_stock,
)

app_name = "stock"

urlpatterns = [
    path("stock/", stock_list_view, name="stock-list"),
    path("stock/transactions", stock_transactions, name="stock-transactions"),
    path("stock/transaction/add/", add_transaction, name="stock-transaction-add"),
    path("stock/add", add_stock, name="stock-add"),
    path(
        "stock/transaction/<str:pk>/edit",
        update_transaction,
        name="stock-update-transaction",
    ),
    path(
        "stock/transaction/<str:pk>/delete/",
        delete_transaction,
        name="stock-delete-transaction",
    ),
]
