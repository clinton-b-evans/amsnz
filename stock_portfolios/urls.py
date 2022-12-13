from django.urls import path
from .views import (
    stock_list_view,
    stock_transactions,
    delete_transaction, add_stock, edit_transaction, edit_sufi_transaction, add_transaction, transaction_list,
)

app_name = "stock"

urlpatterns = [
    path("stock/<str:year>/", stock_list_view, name="stock-list"),
    path("stock/transactions/<str:year>/", stock_transactions, name="stock-transactions"),
    path("stock/transaction/add/", add_transaction, name="add-transaction"),
    path('stock/deleteTransaction',  delete_transaction, name='deleteTransaction'),
    path('stock/addStock', add_stock, name="addStock"),
    path("transaction_list/stock/", transaction_list, name="transaction_list"),
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
