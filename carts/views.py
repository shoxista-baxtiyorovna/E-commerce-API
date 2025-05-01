from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemSerializer, CartSerializer
from .permissions import IsOwner
from .models import Cart, CartItem


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class DeleteCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)



