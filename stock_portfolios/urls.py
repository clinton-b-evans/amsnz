from django.urls import path
from .views import (
    stock_list_view,
    stock_transactions,
    add_transaction,
    delete_transaction, add_stock, edit_transaction, add_sufi_transaction, edit_sufi_transaction,
)

app_name = "stock"

urlpatterns = [
    path("stock/<str:year>/", stock_list_view, name="stock-list"),
    path("stock/transactions/<str:year>/", stock_transactions, name="stock-transactions"),
    path("stock/transaction/add/", add_transaction, name="stock-transaction-add"),
    # path("stock/add", add_stock, name="stock-add"),
    path("stock/addTransaction/", add_transaction, name="addTransaction"),
    path('stock/deleteTransaction',  delete_transaction, name='deleteTransaction'),
    path('stock/addStock', add_stock, name="addStock"),
    path('stock/add_sufi_transaction', add_sufi_transaction, name="add-sufi-transaction"),
    path('stock/edit_sufi_transaction/<pk>/', edit_sufi_transaction, name="edit-sufi-transaction"),
    path(
        "stock/edit",
        edit_transaction,
        name="stock-edit",
    ),
    # path(
    #     "stock/transaction/<str:pk>/delete/",
    #     delete_transaction,
    #     name="stock-delete-transaction",
    # ),
]
