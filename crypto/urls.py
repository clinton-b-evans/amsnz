from django.urls import path
from .views import (
    crypto_list_view,
    add_crypto,
    update_crypto,
    delete_crypto,
    crypto_transactions,
    add_transaction,
    update_transaction,
    delete_transaction
)

app_name = "crypto"

urlpatterns = [
    path("crypto/", crypto_list_view, name="crypto-list"),
    path("crypto/transactions", crypto_transactions, name="crypto-transactions"),
    path("crypto/transaction/add/", add_transaction, name="crypto-transaction-add"),
    path("crypto/add", add_crypto, name="crypto-add"),
    path("crypto/<str:pk>/edit", update_crypto, name="update-crypto"),
    path("crypto/<str:pk>/delete", delete_crypto, name="delete-crypto"),
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
