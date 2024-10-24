# orders/views.py

from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from django.db import transaction
from users.authentication import JWTAuthentication
from .models import Order
from products.models import Product
from users.models import User
from rest_framework.permissions import IsAuthenticated

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication

    @transaction.atomic  # Ensures database consistency (either all changes happen, or none do)
    def post(self, request):
        # Extract user from request using JWT authentication
        user = request.user
        
        # Extract product ID and quantity from the request data
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided
        
        # Validate the product ID
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")
        
        # Check if the requested quantity is available
        if quantity > product.quantity:
            return Response(
                {
                    "detail": f"Only {product.quantity} units available for {product.name}."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Create the order and update the product quantity
        with transaction.atomic():
            order = Order.objects.create(user=user, product=product, quantity=quantity)
            product.quantity -= quantity
            product.save()

        # Prepare the response data
        response_data = {
            'user_id': user.id,
            'user_email': user.email,
            'product_id': order.product.id,
            'product_name': order.product.name,
            'ordered_quantity': order.quantity,
            'remaining_product_quantity': product.quantity,
            'created_at': order.created_at.isoformat()
        }

        return Response(response_data, status=201)
