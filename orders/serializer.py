from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=100, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'shipping_address', 'payment_method', 'total_price', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = representation(many=True, read_only=True)
    status = serializers.CharField(source='orders.status', read_only=True)
    shipping_address = serializers.CharField(source='orders.shipping_address', read_only=True)
    payment_method = serializers.CharField(source='orders.payment_method', read_only=True)
    total_price = serializers.DecimalField(max_digits=100, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(source='orders.created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='orders.updated_at', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'user',
            'items',
            'status',
            'shipping_address',
            'payment_method',
            'product','quantity',
            'total_price',
            'created_at',
            'updated_at'
        ]

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            product = instance.product
            representation['product'] = {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
            return representation