from rest_framework import generics
from rest_framework.filters import SearchFilter
from .serializers import ProductSerializer, ProductDetailSerializer
from .pagination import ProductPagination
from .models import Product


class CustomSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return ['q']

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
    filter_backends = (CustomSearchFilter,)
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.query_params.get('q', None)
        if search_param:
            queryset = (
                        queryset.filter(name__icontains=search_param) |
                        queryset.filter(description__icontains=search_param) |
                        queryset.filter(category__name__icontains=search_param)
                        )
        return queryset