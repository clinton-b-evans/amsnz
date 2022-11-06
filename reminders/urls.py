from django.urls import path
from .views import (
    home_view,
    reminder_list_view,
    add_reminder,
    update_reminder,
    delete_reminder,
    get_reminders,
    current_datetime
)

app_name = "reminders"

urlpatterns = [
    path("reminders/", reminder_list_view, name="reminders_list"),
    path("reminders/add_reminder", add_reminder, name="add-reminder"),
    path("reminders/add_reminder/<str:pk>/", update_reminder, name="update-reminder"),
    path("reminders/<str:pk>/delete", delete_reminder, name="delete-reminder"),
    path("get_reminders/", get_reminders, name="get-reminders"),
]
