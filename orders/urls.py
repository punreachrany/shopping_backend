# orders/urls.py
from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    # path('all/', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='create-order')
]