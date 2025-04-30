from rest_framework import generics
from .serializers import OrderSerializer, ProductOrderSerializer
from .models import Order


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ProductOrderSerializer


