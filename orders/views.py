# orders/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound

from users.authentication import JWTAuthentication
from .models import Order
from products.models import Product
from users.models import User
from rest_framework.permissions import IsAuthenticated

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication

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

        # Create the order
        order = Order.objects.create(user=user, product=product, quantity=quantity)

        # Prepare the response data
        response_data = {
            'user_id': user.id,
            'user_email': user.email,
            'product_id': order.product.id,
            'product_name': order.product.name,
            'quantity': order.quantity,
            'created_at': order.created_at.isoformat()
        }

        return Response(response_data, status=201)
