# orders/serializers.py
from rest_framework import serializers
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product_name', 'quantity', 'price', 'created_at']
        read_only_fields = ['user', 'created_at']
