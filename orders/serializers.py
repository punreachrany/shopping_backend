from rest_framework import serializers
from .models import Order, OrderHistory

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product_name', 'user_email', 'quantity', 'total_price', 'created_at']

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'user', 'order_list', 'date', 'total_price']
