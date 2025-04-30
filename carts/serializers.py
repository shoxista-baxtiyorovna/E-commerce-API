from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cart, CartItem, Product


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity', 'total_price']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product not found.")
        return value

    def create(self, validated_data):
        cart = validated_data['cart']
        product_id = validated_data.pop('product_id')
        quantity = validated_data.pop('quantity')
        product = Product.objects.get(id=product_id)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )

        return cart_item

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = {
            'id': instance.product.id,
            'name': instance.product.name,
            'price': instance.product.price
        }
        return representation



class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']

