from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product

class Inventory(models.Model):
    class SourceType(models.TextChoices):
        FARM = 'FARM', _('Farm')
        BUTCHERY = 'BUTCHERY', _('Butchery')

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='inventory_records'
    )
    source_type = models.CharField(
        max_length=10, 
        choices=SourceType.choices
    )
    quantity_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    minimum_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=10.00
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Inventories")
        unique_together = ('product', 'source_type')

    @property
    def is_low_stock(self):
        return self.quantity_kg <= self.minimum_threshold

    @property
    def availability_status(self):
        if self.quantity_kg <= 0:
            return "OUT_OF_STOCK"
        elif self.is_low_stock:
            return "LOW_STOCK"
        return "IN_STOCK"

    def __str__(self):
        return f"{self.product.name} ({self.get_source_type_display()}): {self.quantity_kg}kg"
