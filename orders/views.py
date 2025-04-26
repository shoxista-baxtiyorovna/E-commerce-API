from rest_framework import generics
from .serializer import OrderSerializer
from .models import Order


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

