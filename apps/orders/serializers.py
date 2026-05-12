from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem, Cart, CartItem, Contract
from apps.products.models import Product
from apps.inventory.models import Inventory

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = (
            'id', 'product', 'product_name', 'quantity_kg', 
            'price_per_kg', 'subtotal', 'inventory_source'
        )
        read_only_fields = ('price_per_kg', 'subtotal')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'user_name', 'status', 'total_amount', 
            'delivery_address', 'payment_status', 'scheduled_for', 
            'created_at', 'items'
        )
        read_only_fields = ('user', 'total_amount', 'status', 'payment_status')

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        
        total_amount = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity_kg']
            source = item_data.get('inventory_source', Inventory.SourceType.FARM)
            
            # Wholesale pricing logic
            is_bulk = user.role == 'BUSINESS_CUSTOMER' and product.is_bulk_available
            if is_bulk and product.bulk_price_per_kg:
                price = product.bulk_price_per_kg
            else:
                price = product.price_per_kg
                is_bulk = False
            
            # Check inventory (Basic check)
            try:
                inventory = Inventory.objects.get(product=product, source_type=source)
                if inventory.quantity_kg < quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name} at {source}."
                    )
                # Deduct stock (as per Option 1 — Deduct After Payment/Order logic)
                inventory.quantity_kg -= quantity
                inventory.save()
            except Inventory.DoesNotExist:
                raise serializers.ValidationError(
                    f"Inventory record for {product.name} at {source} does not exist."
                )

            item_total = price * quantity
            total_amount += item_total
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity_kg=quantity,
                price_per_kg=price,
                subtotal=item_total,
                inventory_source=source,
                is_bulk=is_bulk
            )
            
        order.total_amount = total_amount
        order.save()
        return order

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    price_per_kg = serializers.ReadOnlyField(source='product.price_per_kg')

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'quantity_kg', 'price_per_kg', 'inventory_source')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price')

    def get_total_price(self, obj):
        return sum(item.product.price_per_kg * item.quantity_kg for item in obj.items.all())

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('user',)
