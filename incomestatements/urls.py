from django.urls import path
from .views import (
    incomestatements_list_view,
    add_incomestatements,
    update_incomestatements,
    delete_incomestatement,
    add_category,
    update_category,
    year_to_date,
)

app_name = "incomestatements"

urlpatterns = [
    path("incomestatements/", incomestatements_list_view, name="incomestatement-list"),
    path("incomestatements/add", add_incomestatements, name="incomestatement-add"),
    path("incomestatements/add_category", add_category, name="category-add"),
    path(
        "incomestatements/<str:pk>/edit",
        update_incomestatements,
        name="update-incomestatement",
    ),
    path(
        "incomestatements/<str:pk>/delete",
        delete_incomestatement,
        name="delete-incomestatement",
    ),
    path(
        "incomestatements/<str:pk>/edit_category",
        update_category,
        name="update-category",
    ),
    path("incomestatements/yeartodate/<str:year>/", year_to_date, name="year-to-date"),
]
