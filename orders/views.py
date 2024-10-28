# orders/views.py

from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from django.db import transaction
from orders.serializers import OrderHistorySerializer, OrderSerializer
from users.authentication import JWTAuthentication
from .models import Order, OrderHistory
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
    
class GetAllOrderHistory(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        order_history = OrderHistory.objects.filter(user=request.user).order_by('-date')
        serializer = OrderHistorySerializer(order_history, many=True)
        return Response(serializer.data, status=200)

class GetOrderByMonth(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, month, year):
        order_history = OrderHistory.objects.filter(user=request.user, date__month=month, date__year=year)
        serializer = OrderHistorySerializer(order_history, many=True)
        return Response(serializer.data, status=200)

class GetOrderByYear(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, year):
        order_history = OrderHistory.objects.filter(user=request.user, date__year=year)
        serializer = OrderHistorySerializer(order_history, many=True)
        return Response(serializer.data, status=200)
    
class GetChartListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        product_list = request.data.get('product_list', [])
        chart_list = []
        total_price = 0.0

        for item in product_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Product with id {product_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if quantity > product.quantity:
                return Response(
                    {"detail": f"Only {product.quantity} units available for {product.name}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            price = product.price * quantity
            total_price += price
            chart_list.append({
                "product": product.name,
                "quantity": quantity,
                "price": price
            })

        return Response({
            "chart_list": chart_list,
            "total_price": total_price
        }, status=status.HTTP_200_OK)


class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):
        product_list = request.data.get('product_list', [])
        total_price = 0.0

        # Validate products and calculate total price
        for item in product_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Product with id {product_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if quantity > product.quantity:
                return Response(
                    {"detail": f"Only {product.quantity} units available for {product.name}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_price += product.price * quantity

        # Create OrderHistory record
        order_history = OrderHistory.objects.create(user=request.user, total_price=total_price)

        # Create orders and update product quantities
        for item in product_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            product = Product.objects.get(id=product_id)

            # Create Order
            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_price=product.price * quantity,
            )

            # Update product quantity
            product.quantity -= quantity
            product.save()

            # Add order to order history
            order_history.order_list.add(order)

        return Response({"detail": "Purchase successful.", "total_price": total_price}, status=status.HTTP_201_CREATED)