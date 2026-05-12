from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.orders.models import Order

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='addresses'
    )
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.district}, {self.sector}, {self.cell}"

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Assignment')
        ASSIGNED = 'ASSIGNED', _('Driver Assigned')
        IN_TRANSIT = 'IN_TRANSIT', _('In Transit')
        DELIVERED = 'DELIVERED', _('Delivered')
        FAILED = 'FAILED', _('Delivery Failed')

    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        related_name='delivery'
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='deliveries',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    estimated_time = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Deliveries")

    def __str__(self):
        return f"Delivery for Order #{self.order.id} ({self.get_status_display()})"
