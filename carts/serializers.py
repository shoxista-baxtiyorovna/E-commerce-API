from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cart, CartItem
from products.models import Product


#
# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = instance.product
        representation['product'] = {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
        return representation


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
