from rest_framework import serializers
from .models import Cart, CartItem


class CartSerializer(serializers.Serializer):
