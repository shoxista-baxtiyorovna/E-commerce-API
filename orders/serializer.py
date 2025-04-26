from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=100, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'shipping_address', 'payment_method', 'total_price', 'created_at', 'updated_at']