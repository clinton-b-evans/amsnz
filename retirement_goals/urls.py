from django.urls import path
from .views import (
    update_retirementgoal,
)

app_name = 'retirement_goals'

urlpatterns = [
    path('retiregoals/',update_retirementgoal, name='update_retirementgoal'),


]