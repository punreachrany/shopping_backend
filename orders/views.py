# orders/views.py

from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from django.db import transaction
from orders.serializers import OrderSerializer
from users.authentication import JWTAuthentication
from .models import Order
from products.models import Product
from users.models import User
from rest_framework.permissions import IsAuthenticated

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):
        user = request.user

        # Extract product ID and quantity from the request
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        # Validate product existence
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

        # Check if the requested quantity is available
        if quantity > product.quantity:
            return Response(
                {"detail": f"Only {product.quantity} units available for {product.name}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate total price
        total_price = product.price * quantity

        # Create the order and update product quantity
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
            )
            product.quantity -= quantity
            product.save()

        # Prepare response data
        response_data = {
            'user_id': user.id,
            'user_email': user.email,
            'product_id': product.id,
            'product_name': product.name,
            'ordered_quantity': quantity,
            'total_price': total_price,
            'remaining_product_quantity': product.quantity,
            'created_at': order.created_at.isoformat(),
        }

        return Response(response_data, status=201)

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Fetch all orders for the authenticated user
        orders = Order.objects.filter(user=request.user)

        # Serialize the orders
        serializer = OrderSerializer(orders, many=True)
        
        # Calculate total price of all orders
        total_price = sum(order['total_price'] for order in serializer.data)

        # Prepare the response data
        response_data = {
            "order": serializer.data,
            "status": "success",  # or "failed" based on your logic
            "total_price": total_price,
        }

        return Response(response_data, status=200)