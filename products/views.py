from rest_framework import generics
from rest_framework.filters import SearchFilter
from .serializers import ProductSerializer, ProductDetailSerializer
from .pagination import ProductPagination
from .models import Product


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name', 'description', 'category__name']

