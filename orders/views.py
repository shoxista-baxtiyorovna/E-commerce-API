from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.filter(user=user).first()

        if not order:
            return Response(
                {"detail": "Order not found for the user."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_item = serializer.save(cart=order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

