from django.urls import path
from .views import (
    personal_balance_list_view,
    personal_balance_list_weekly,
    personal_balance_list_monthly,
    add_personal_balance,
    update_personal_balance,
    delete_personal_balance, addpersonal_balance, updatepersonal_balance, deletepersonal_balance,
)

app_name = "personal_balances"

urlpatterns = [
    path(
        "personal_balances/", personal_balance_list_view, name="personal_balances_list"
    ),
    path("personal_balances/weekly", personal_balance_list_weekly, name="weekly-list"),
    path(
        "personal_balances/monthly", personal_balance_list_monthly, name="monthly-list"
    ),
    path("personal_balances/add", add_personal_balance, name="personal-balance-add"),
    path(
        "personal_balances/<str:pk>/edit",
        update_personal_balance,
        name="update-personal-balance",
    ),
    path(
        "addpersonal_balance",
        addpersonal_balance,
        name="addpersonal_balance",
    ),
    path(
        "updatepersonal_balance",
        updatepersonal_balance,
        name="updatepersonal_balance",
    ),
    path(
        "deletepersonal_balance",
        deletepersonal_balance,
        name="deletepersonal_balance",
    ),

    path(
        "personal_balances/<str:pk>/delete",
        delete_personal_balance,
        name="delete-personal-balance",
    ),
]
