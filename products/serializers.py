from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(read_only=True)  # Read-only price field

    class Meta:
        model = Product
        fields = '__all__'  # Includes all model fields
