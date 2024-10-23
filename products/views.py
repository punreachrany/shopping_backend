# products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer

class ProductListView(APIView):
    def get(self, request):
        category_name = request.query_params.get('category')
        search_query = request.query_params.get('search')

        products = Product.objects.all()

        if category_name:
            products = products.filter(category__name__icontains=category_name)
        if search_query:
            products = products.filter(name__icontains=search_query)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
