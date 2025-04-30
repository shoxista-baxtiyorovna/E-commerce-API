from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CartItemSerializer, CartSerializer
from .models import Cart


class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
