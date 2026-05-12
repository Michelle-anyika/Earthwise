from rest_framework import serializers
from .models import Address, Delivery

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id', 'user', 'district', 'sector', 'cell', 
            'street', 'notes', 'latitude', 'longitude', 'is_default'
        )
        read_only_fields = ('user',)

class DeliverySerializer(serializers.ModelSerializer):
    order_details = serializers.ReadOnlyField(source='order.id')
    driver_name = serializers.ReadOnlyField(source='driver.username')

    class Meta:
        model = Delivery
        fields = (
            'id', 'order', 'order_details', 'driver', 'driver_name', 
            'status', 'estimated_time', 'delivered_at'
        )
        read_only_fields = ('order',)
