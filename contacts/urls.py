from django.urls import path
from .views import (
    home_view,
    contact_list_view,
    add_contact,
    update_contact,
    delete_contact,
)

app_name = "contacts"

urlpatterns = [
    path("contacts/", contact_list_view, name="contacts_list"),
    path("contacts/add", add_contact, name="add-contact"),
    path("contacts/<str:pk>/edit", update_contact, name="update-contact"),
    path("contacts/<str:pk>/delete", delete_contact, name="delete-contact"),
]
