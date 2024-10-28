# orders/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('history/', OrderHistoryView.as_view(), name='order_history'),
    path('history/all/', GetAllOrderHistory.as_view(), name='get-all-order-history'),  # New
    path('history/month/<int:month>/<int:year>/', GetOrderByMonth.as_view(), name='get-order-by-month'),  # New
    path('history/year/<int:year>/', GetOrderByYear.as_view(), name='get-order-by-year'),  # New
    path('chart/', GetChartListView.as_view(), name='get-chart-list'),  # New
    path('purchase/', PurchaseView.as_view(), name='purchase'),  # New
]