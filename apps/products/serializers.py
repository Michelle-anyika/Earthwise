from rest_framework import serializers
from .models import ProductCategory, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description', 'product_count')

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'category_name', 'name', 'description', 
            'price_per_kg', 'bulk_price_per_kg', 'is_bulk_available', 
            'image', 'is_active', 'product_type'
        )
