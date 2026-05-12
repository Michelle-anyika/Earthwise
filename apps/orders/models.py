from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product
from apps.inventory.models import Inventory

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        PREPARING = 'PREPARING', _('Preparing')
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', _('Out for Delivery')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', _('Unpaid')
        PAID = 'PAID', _('Paid')
        REFUNDED = 'REFUNDED', _('Refunded')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_address = models.TextField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=20, 
        choices=PaymentStatus.choices, 
        default=PaymentStatus.UNPAID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Price snapshotting
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    inventory_source = models.CharField(
        max_length=10, 
        choices=Inventory.SourceType.choices,
        default=Inventory.SourceType.FARM
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity_kg * self.price_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity_kg}kg in Order #{self.order.id}"

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    inventory_source = models.CharField(
        max_length=10, 
        choices=Inventory.SourceType.choices,
        default=Inventory.SourceType.FARM
    )

    class Meta:
        unique_together = ('cart', 'product', 'inventory_source')

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"
