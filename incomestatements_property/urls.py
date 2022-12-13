from django.urls import path

from incomestatements.views import add_category
from .views import (
    incomestatement_property_list_view,
    delete_property_incomestatement,
    year_to_date, addproperty_incomestatements, addcategory_incomestatements, editproperty_incomestatements,
    deleteproperty_incomestatement, category_list, edit_category, delete_category,
)

app_name = "incomestatements_property"

urlpatterns = [
    path(
        "propertyincomestatements/<str:year>/",
        incomestatement_property_list_view,
        name="property-incomestatement-list",
    ),
    path(
        "addcategory/",
        addcategory_incomestatements,
        name="addcategory",
    ),
    path(
        "propert_forecast/<str:year>/",
        category_list,
        name="propert_forecast",
    ),
    path(
        "editcategory/",
        edit_category,
        name="editcategory",
    ),
    path(
        "deletecategory/",
        delete_category,
        name="deletecategory",
    ),
    path(
        "addproperty/",
        addproperty_incomestatements,
        name="addproperty",
    ),
    path(
        "editproperty/",
        editproperty_incomestatements,
        name="editproperty",
    ),
    path(
        "propertyincomestatements/<str:pk>/delete",
        delete_property_incomestatement,
        name="delete_property_incomestatement",
    ),
    path(
        "propertyincomestatements/delete",
        deleteproperty_incomestatement,
        name="deleteproperty_incomestatement",
    ),
    path(
        "propertyincomestatements/yeartodate/<str:year>/",
        year_to_date,
        name="property_year-to-date",
    ),
]
