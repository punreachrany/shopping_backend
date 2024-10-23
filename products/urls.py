# products/urls.py
from django.urls import path
from .views import list_products, create_product, product_detail

urlpatterns = [
    path('all', list_products, name='product-list'),            # Endpoint for listing products
    path('create', create_product, name='product-create'),      # Endpoint for creating a product
    path('<int:pk>', product_detail, name='product-detail'),    # Endpoint for product details by ID
]
