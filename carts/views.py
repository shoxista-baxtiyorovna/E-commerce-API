from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from common.throttling import PremiumUserRateThrottle
from .serializers import CartItemSerializer, CartSerializer
from .permissions import IsOwner
from .models import Cart, CartItem


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]


class DeleteCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_throttles(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_premium:
            throttle_classes = [PremiumUserRateThrottle]
        else:
            throttle_classes = [UserRateThrottle]
        return [throttle() for throttle in throttle_classes]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)



