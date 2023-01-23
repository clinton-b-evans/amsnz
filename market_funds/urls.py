from django.urls import path
from .views import (
    fund_list_view,
    add_indexfund,
    update_indexfund,
    delete_indexfund,
    add_trade,
    indexfund_detail_view,
)

app_name = "market_funds"

urlpatterns = [
    path("marketfunds/<str:year>/", fund_list_view, name="Index_fund_list"),
    path("marketfund/<str:pk>/", indexfund_detail_view, name="fund-detail"),
    path("marketfunds/add", add_indexfund, name="fund-add"),
    path("trade/add", add_trade, name="trade-add"),
    path("marketfunds/<str:pk>/edit", update_indexfund, name="update-indexfund"),
    path("marketfunds/<str:pk>/delete", delete_indexfund, name="delete-indexfund"),
]
