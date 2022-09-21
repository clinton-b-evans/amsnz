from django.urls import path
from .views import (
    cash_flow_list_view,
    cash_flow_weekly_view,
    cash_flow_yearly_view,
    add_cash_flow,
    update_cash_flow,
    delete_cash_flow,
)

app_name = 'cash_flows'

urlpatterns = [
    path('cashflows/', cash_flow_list_view, name='cashflow-list'),
    path('cashflows/weekly', cash_flow_weekly_view, name='cashflow-weekly-list'),
    path('cashflows/yearly', cash_flow_yearly_view, name='cashflow-yearly-list'),
    path('cashflows/add', add_cash_flow, name='cashflow-add'),
    path('cashflows/<str:pk>/edit',update_cash_flow, name='update-cashflow'),
    path('cashflows/<str:pk>/delete',delete_cash_flow, name='delete-cashflow'),

]