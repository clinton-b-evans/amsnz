from django.urls import path
from .views import (
    home_view,
    reminder_list_view,
    add_reminder,
    update_reminder,
    delete_reminder,
    addreminder, editreminder, deletereminder,
)

app_name = "reminders"

urlpatterns = [
    path("reminders/<str:year>/", reminder_list_view, name="reminders_list"),
    path("reminders/add_reminder", add_reminder, name="add-reminder"),
    path("reminders/add_reminder/<str:pk>/", update_reminder, name="update-reminder"),
    path("reminders/<str:pk>/delete", delete_reminder, name="delete-reminder"),
    path("addreminder/", addreminder, name="addreminder"),
    path("editreminder/", editreminder, name="editreminder"),
    path("deletereminder/", deletereminder, name="deletereminder"),
]
