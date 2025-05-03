from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from common.throttling import PremiumUserRateThrottle, RoleBasedScopedRateThrottle
from .permissions import IsOwner
from .serializers import OrderSerializer, ProductOrderSerializer
from .models import Order


class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ProductOrderSerializer
    throttle_classes = [RoleBasedScopedRateThrottle]
    throttle_scope_general = 'orders-create'
    throttle_scope_premium = 'premium'


class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]


