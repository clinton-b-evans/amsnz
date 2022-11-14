from django.urls import path

from .views import (
    crypto_list_view,
    add_crypto,
    update_crypto,
    delete_crypto,
    crypto_transactions,
    add_transaction,
    update_transaction,
    delete_transaction,
    edit_transaction, crudview, get, update, addTransaction, deleteTransaction
)

app_name = "crypto"


class CreateCrudUser:
    pass


urlpatterns = [
    path("crypto/", crypto_list_view, name="crypto-list"),
    path("crypto/transactions", crypto_transactions, name="crypto-transactions"),
    path("crypto/transaction/add/", add_transaction, name="crypto-transaction-add"),
    path("crypto/addTransaction/", addTransaction, name="addTransaction"),
    path('crypto/deleteTransaction/',  deleteTransaction, name='deleteTransaction'),
    path("crypto/add", add_crypto, name="crypto-add"),
    path("crypto/<str:pk>/edit", update_crypto, name="update-crypto"),
    path('crypto/crud/', crudview, name='crud_ajax'),
    path('ajax/crud/create/', get, name='crud_ajax_create'),
    path('ajax/crud/update/',  update, name='crud_ajax_update'),
    path("crypto/<str:pk>/delete", delete_crypto, name="delete-crypto"),
    path(
        "crypto/edit",
        edit_transaction,
        name="crypto-edit",
    ),
    path(
        "crypto/transaction/<str:pk>/edit",
        update_transaction,
        name="crypto-update-transaction",
    ),
    path(
        "crypto/transaction/<str:pk>/delete/",
        delete_transaction,
        name="crypto-delete-transaction",
    ),
]
