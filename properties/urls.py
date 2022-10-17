from django.urls import path
from django.views.generic import RedirectView

from .views import (
    home_view,
    property_list_view,
    property_list_monthly,
    property_list_weekly,
    property_detail_view,
    property_summary_view,
    add_property,
    update_property,
    delete_property,
    pam_home_view,
)

app_name = "properties"

urlpatterns = [
    path("properties/", property_list_view, name="list"),
    path("properties/weekly/", property_list_weekly, name="weekly-list"),
    path("properties/monthly/", property_list_monthly, name="monthly-list"),
    path("summary/<str:year>/", property_summary_view, name="summary"),
    path("properties/<pk>/", property_detail_view, name="detail"),
    path("properties/add", add_property, name="add-property"),
    path("properties/<str:pk>/edit", update_property, name="update-property"),
    path("properties/<str:pk>/delete", delete_property, name="delete-property"),
]
