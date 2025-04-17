from rest_framework import serializers
from categories.models import Category
from .models import Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'in_stock',
            'quantity',
            'created_at',
            'updated_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'in_stock',
            'quantity',
            'created_at',
            'updated_at'
        ]