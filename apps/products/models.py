from django.db import models
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    bulk_price_per_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    is_bulk_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Optional field for Farm vs Butcher
    PRODUCT_TYPE_CHOICES = [
        ('FARM', 'Farm Product'),
        ('BUTCHER', 'Butcher Product'),
    ]
    product_type = models.CharField(
        max_length=10, 
        choices=PRODUCT_TYPE_CHOICES, 
        default='FARM'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
