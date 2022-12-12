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
    commodity_transactions,
    get_commodities, addTransaction, edit_transaction, deleteTransaction, edit_sufi_transaction, add_sufi_transaction,
    commodity_transaction_list
)

app_name = "commodities"


urlpatterns = [
    # path("commodities/<str:year>/", commodity_list_view, name="commodities_list"),
    path("commodities/add", add_commodity, name="add"),
    # path("commodities/transaction/add/", add_transaction, name="transaction-add"),
    path('commodities/deleteTransaction/',  deleteTransaction, name='deleteTransaction'),
    # path("commodities/<pk>/", commodity_detail_view, name="detail"),
    path("commodities/addTransaction/", addTransaction, name="addTransaction"),
    path("commodities/<str:pk>/edit", update_commodity, name="update"),
    path("transaction_list/", commodity_transaction_list, name="commodity_transaction_list"),
    path('commodities/edit_sufi_transaction/<pk>/', edit_sufi_transaction, name="edit-sufi-transaction"),
    path("commodities/transaction/add/", add_sufi_transaction, name="add-sufi-transaction"),
    path(
        "commodities/transaction/<str:pk>/edit",
        update_transaction,
        name="update-transaction",
    ),
    path(
        "commodities/edit",
        edit_transaction,
        name="commodity-edit",
    ),
    path("commodities/<str:pk>/delete/", delete_commodity, name="delete"),
    # path(
    #     "commodities/transaction/<str:pk>/delete/",
    #     delete_transaction,
    #     name="delete-transaction",
    # ),
    path(
        "commodities-classes/",
        commodity_transactions,
        name="commodities_transactions",
    ),
    path(
        "commodities-classes/<str:year>/",
        commodity_transactions,
        name="commodities_classes",
    ),
    path(
        "get_commodities/",
        get_commodities,
        name="get_commodities",
    ),

    path("commodities/<str:year>/", commodity_list_view, name="commodities_list"),
]
