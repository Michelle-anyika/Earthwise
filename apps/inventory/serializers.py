from rest_framework import serializers
from .models import Inventory
from apps.products.serializers import ProductSerializer

class InventorySerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    availability_status = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = (
            'id', 'product', 'product_details', 'source_type', 
            'quantity_kg', 'minimum_threshold', 'is_low_stock', 
            'availability_status', 'last_updated'
        )
