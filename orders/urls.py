# orders/urls.py
from django.urls import path
from .views import CreateOrderView, OrderHistoryView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('history/', OrderHistoryView.as_view(), name='order_history'),
]