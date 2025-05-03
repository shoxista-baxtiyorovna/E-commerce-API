from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import AllowAny
from common.throttling import PremiumUserRateThrottle, RoleBasedScopedRateThrottle
from .serializers import ProductSerializer, ProductDetailSerializer
from .pagination import ProductPagination
from .models import Product


class CustomSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return ['q']

@method_decorator(cache_page(60*1), name='dispatch')
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]

    def get_throttles(self):
        if self.request.user.is_authenticated:
            if self.request.user.profile.is_premium:
                throttle_classes = [PremiumUserRateThrottle]
            else:
                throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = [AnonRateThrottle]
        return [throttle() for throttle in throttle_classes]


@method_decorator(cache_page(60*1), name='dispatch')
class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_throttles(self):
        if self.request.user.is_authenticated:
            if self.request.user.profile.is_premium:
                throttle_classes = [PremiumUserRateThrottle]
            else:
                throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = [AnonRateThrottle]
        return [throttle() for throttle in throttle_classes]


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]
    filter_backends = (CustomSearchFilter,)
    search_fields = ['name', 'description']
    throttle_classes = [RoleBasedScopedRateThrottle]
    throttle_scope_general = 'products-search'
    throttle_scope_premium = 'premium'

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