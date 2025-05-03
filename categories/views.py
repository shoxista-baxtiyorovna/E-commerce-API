from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from common.throttling import PremiumUserRateThrottle
from .serializers import CategorySerializer
from .pagination import CategoryPagination
from .models import Category


@method_decorator(cache_page(60*60), name='dispatch')
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
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


@method_decorator(cache_page(60*60), name='dispatch')
class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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