from django.urls import path
from .views import (
    incomestatements_list_view,
    add_incomestatements,
    update_incomestatements,
    delete_incomestatement,
    add_category,
    update_category,
    year_to_date, addcategory_incomestatements, addproperty_incomestatements, editproperty_incomestatements,
    deleteproperty_incomestatement,
)

app_name = "incomestatements"

urlpatterns = [
    path("incomestatements/", incomestatements_list_view, name="incomestatements"),
    path("incomestatements/add", add_incomestatements, name="incomestatement-add"),
    path("incomestatements/add_category", add_category, name="category-add"),
    path(
        "incomestatements/<str:pk>/edit",
        update_incomestatements,
        name="update-incomestatement",
    ),
    path(
        "addcategory_incomestatements",
        addcategory_incomestatements,
        name="addcategory_incomestatements",
    ),
    path(
        "addproperty_incomestatements",
        addproperty_incomestatements,
        name="addproperty_incomestatements",
    ),
    path(
        "editproperty_incomestatements",
        editproperty_incomestatements,
        name="editproperty_incomestatements",
    ),
    path(
        "deleteproperty_incomestatement",
        deleteproperty_incomestatement,
        name="deleteproperty_incomestatement",
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
    path(
        "incomestatements/yeartodate/<str:year>/",
        year_to_date,
        name="incomestatement_year_to_date",
    ),
]
