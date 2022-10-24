from django.urls import path
from .views import (
    crypto_list_view,
    add_crypto,
    update_crypto,
    delete_crypto,
)

app_name = "crypto"

urlpatterns = [
    path("crypto/<str:year>/", crypto_list_view, name="crypto-list"),
    path("crypto/add", add_crypto, name="crypto-add"),
    path("crypto/<str:pk>/edit", update_crypto, name="update-crypto"),
    path("crypto/<str:pk>/delete", delete_crypto, name="delete-crypto"),
]
