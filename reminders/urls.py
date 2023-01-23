from django.urls import path
from .views import (
    home_view,
    reminder_list_view,
    add_reminder,
    update_reminder,
    delete_reminder,
    add_reminder, edit_reminder, deletereminder, notifications_view, notifications_list, update_notifications,
    notifications_table_list, data_list,
)

app_name = "reminders"

urlpatterns = [
    path("reminders/<str:year>/", reminder_list_view, name="reminders_list"),
    path("reminders/add_reminder", add_reminder, name="add-reminder"),
    path("reminders/edit_reminder/<str:pk>/", edit_reminder, name="update-reminder"),
    path("reminders/<str:pk>/delete", delete_reminder, name="delete-reminder"),
    path("addreminder/", add_reminder, name="add-reminder"),
    path("editreminder/<str:pk>/", edit_reminder, name="edit-reminder"),
    path("deletereminder/", deletereminder, name="deletereminder"),
    path("notifications/", notifications_view, name="notifications-view"),
    path("list/", notifications_list, name="notification-list"),
    path("table_list/", notifications_table_list, name="table-list"),
    path("reminders/update_notifications/<str:id>/", update_notifications, name="update-notifications"),
    path(
        "data_list/reminder",
        data_list,
        name="data_list_reminder",
    ),
]
