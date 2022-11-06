from django.urls import path
from .views import (
    crypto_list_view,
    add_crypto,
    update_crypto,
    delete_crypto,
    crypto_transactions
)

app_name = "crypto"

urlpatterns = [
    path("crypto/", crypto_list_view, name="crypto-list"),
    path("crypto/transactions", crypto_transactions, name="crypto-transactions"),
    path("crypto/add", add_crypto, name="crypto-add"),
    path("crypto/<str:pk>/edit", update_crypto, name="update-crypto"),
    path("crypto/<str:pk>/delete", delete_crypto, name="delete-crypto"),
]
