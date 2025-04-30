from django.contrib.auth.models import User
from rest_framework import serializers

from products.models import Product
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=100, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'shipping_address', 'payment_method', 'total_price', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'name', 'price', 'quantity']

    def get_price(self, obj):
        return obj.total_price


class ProductOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'items', 'shipping_address', 'payment_method',
            'total_price', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ('user',)

    def get_total_price(self, obj):
        return obj.total_price

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=user, **validated_data)

        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price  # store current price
            )

        return order
