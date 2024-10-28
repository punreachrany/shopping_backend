# products/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Get all products
@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Create a new product
@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific product
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Helper function for pagination
def paginate_products(products, number, page):
    start = (page - 1) * number
    end = start + number
    paginated_products = products[start:end]
    return paginated_products

# Get all products with pagination
@api_view(['GET'])
def list_products_paginated(request):
    number = int(request.query_params.get('number', 10))  # Default 10 products per page
    page = int(request.query_params.get('page', 1))  # Default page 1

    products = Product.objects.all()
    paginated_products = paginate_products(products, number, page)
    serializer = ProductSerializer(paginated_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get products by category (all or paginated)
@api_view(['GET'])
def products_by_category(request):
    category = request.query_params.get('category')
    if not category:
        return Response({'error': 'Category is required.'}, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.filter(category=category)

    # Check for pagination parameters
    number = int(request.query_params.get('number', 10))
    page = int(request.query_params.get('page', 1))

    paginated_products = paginate_products(products, number, page)
    serializer = ProductSerializer(paginated_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)