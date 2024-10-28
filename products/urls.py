from django.urls import path
from .views import (
    list_products,
    create_product,
    product_detail,
    list_products_paginated,
    products_by_category,
)

urlpatterns = [
    path('all/', list_products, name='product-list'),            # Endpoint for listing products
    path('create/', create_product, name='product-create'),      # Endpoint for creating a product
    path('<int:pk>/', product_detail, name='product-detail'),    # Endpoint for product details by ID
    path('paginated/', list_products_paginated, name='product-list-paginated'),  # Endpoint for paginated product list
    path('category/', products_by_category, name='products-by-category'),  # Endpoint for products by category
]
