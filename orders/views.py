from rest_framework import generics
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import OrderSerializer, ProductOrderSerializer
from .models import Order


class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ProductOrderSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'orders-create'


class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]


