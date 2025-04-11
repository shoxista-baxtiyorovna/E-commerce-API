from rest_framework import serializers
from .models import Product


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

        # def to_representation(self, instance):
            # data = super().to_representation(instance)


        