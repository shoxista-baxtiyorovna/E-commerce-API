from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'quantity']
    search_fields = ['name', 'price']
