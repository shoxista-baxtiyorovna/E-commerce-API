from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem


class ListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response(
                {"detail": "Cart not found for the user."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cart_item = serializer.save(cart=cart)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)