from django.urls import path
from .views import (
    incomestatements_list_view,
    add_incomestatements,
    update_incomestatements,
    delete_incomestatement,
    add_category,
    update_category,
    year_to_date, addcategory_incomestatements, addproperty_incomestatements, editproperty_incomestatements,
    deleteproperty_incomestatement, show_report, category_list, delete_category, edit_category, data_list,
)

app_name = "incomestatements"

urlpatterns = [
    path("incomestatements/<str:year>/", incomestatements_list_view, name="incomestatements"),
    path("incomestatements/add", add_incomestatements, name="incomestatement-add"),
    path("incomestatements/add_category", add_category, name="category-add"),
    path(
        "incomestatements/<str:pk>/edit",
        update_incomestatements,
        name="update-incomestatement",
    ),
    path(
        "report/<str:category>/<str:year>/",
        show_report,
        name="report",
    ),
    path(
        "data_list/",
        data_list,
        name="data_list",
    ),
    path(
        "addcategory_incomestatements",
        addcategory_incomestatements,
        name="addcategory_incomestatements",
    ),
    path(
        "category_list/<str:year>/",
        category_list,
        name="category_list",
    ),
    path(
        "edit_category/",
        edit_category,
        name="edit_category",
    ),
    path(
        "delete_category/",
        delete_category,
        name="delete_category",
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
