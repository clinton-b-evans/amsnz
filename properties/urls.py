from django.urls import path
from django.views.generic import RedirectView
import datetime

today = datetime.date.today()
year = today.year

from .views import (
    property_list_view,
    property_list_monthly,
    property_list_weekly,
    property_detail_view,
    property_summary_view,
    add_property, property_list, edit_property, remove_property, main,
)

app_name = "properties"

urlpatterns = [
    path("", RedirectView.as_view(url=f"summary/{year}/")),
    path("properties/", main, name="properties"),
    path("property_list/", property_list, name="properties_list"),
    path("properties/weekly/", property_list_weekly, name="weekly-list"),
    path("properties/monthly/", property_list_monthly, name="monthly-list"),
    path("summary/<str:year>/", property_summary_view, name="summary"),
    path("properties/<pk>/", property_detail_view, name="detail"),
    path("properties/add", add_property, name="add-property"),
    path("properties/edit/<pk>/", edit_property, name="edit-property"),
    path("properties/delete/<str:pk>/", remove_property, name="delete-property"),
]
