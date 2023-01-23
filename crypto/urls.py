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
    edit_transaction, crudview, get, update, edit_sufi_transaction, add_sufi_transaction,
    crypto_transaction_list,
)

app_name = "crypto"


class CreateCrudUser:
    pass


urlpatterns = [
    path("crypto/<str:year>/", crypto_list_view, name="crypto-list"),
    path("crypto/transactions/<str:year>/", crypto_transactions, name="crypto-transactions"),
    # path("crypto/transaction/add/", add_transaction, name="crypto-transaction-add"),
    # path("crypto/addTransaction", add_transaction, name="addTransaction"),
    path('crypto/deleteTransaction',  delete_transaction, name='deleteTransaction'),
    path("crypto/add", add_crypto, name="crypto-add"),
    path("crypto/<str:pk>/edit", update_crypto, name="update-crypto"),
    path('crypto/crud/', crudview, name='crud_ajax'),
    path('ajax/crud/create/', get, name='crud_ajax_create'),
    path("transaction_list/", crypto_transaction_list, name="crypto_transaction_list"),
    path('ajax/crud/update/',  update, name='crud_ajax_update'),
    path('crypto/addCrypto', add_crypto, name='addCrypto'),
    path("crypto/<str:pk>/delete", delete_crypto, name="delete-crypto"),
    path('crypto/edit_sufi_transaction/<pk>/', edit_sufi_transaction, name="edit-sufi-transaction"),
    path("crypto/transaction/add/", add_sufi_transaction, name="add-sufi-transaction"),
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
