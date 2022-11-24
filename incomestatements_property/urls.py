from django.urls import path
from .views import (
    incomestatement_property_list_view,
    add_property_incomestatements,
    add_property_category,
    update_property_incomestatements,
    delete_property_incomestatement,
    year_to_date, addproperty_incomestatements, addcategory_incomestatements, editproperty_incomestatements,
    deleteproperty_incomestatement,
)

app_name = "incomestatements_property"

urlpatterns = [
    path(
        "propertyincomestatements/",
        incomestatement_property_list_view,
        name="property-incomestatement-list",
    ),
    path(
        "addcategory/",
        addcategory_incomestatements,
        name="addcategory",
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
        "propertyincomestatements/add",
        add_property_incomestatements,
        name="add_property_incomestatements",
    ),

    path(
        "propertyincomestatements/add_category",
        add_property_category,
        name="add_property_category",
    ),
    path(
        "propertyincomestatements/<str:pk>/edit",
        update_property_incomestatements,
        name="update_property_category",
    ),
    path(
        "propertyincomestatements/<str:pk>/delete",
        delete_property_incomestatement,
        name="delete_property_incomestatement",
    ),
    path(
        "propertyincomestatements//delete",
        deleteproperty_incomestatement,
        name="deleteproperty_incomestatement",
    ),
    path(
        "propertyincomestatements/yeartodate/<str:year>/",
        year_to_date,
        name="property_year-to-date",
    ),
]
