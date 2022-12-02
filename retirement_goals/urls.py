from django.urls import path
from .views import (
    update_retirementgoal, add_retirement_goal,
)

app_name = "retirement_goals"

urlpatterns = [
    path("retiregoals/", update_retirementgoal, name="update_retirementgoal"),
    path("add_retirement_goal/", add_retirement_goal, name="add_retirement_goal"),
]
