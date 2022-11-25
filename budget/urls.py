from django.urls import path
from .views import (

    budget_list_view
)

app_name = "budget"


urlpatterns = [
    path("budget_list/<str:year>/", budget_list_view, name="budget_list"),

]
