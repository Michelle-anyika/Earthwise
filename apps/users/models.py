from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', _('Customer')
        BUSINESS_CUSTOMER = 'BUSINESS_CUSTOMER', _('Business Customer')
        STAFF = 'STAFF', _('Staff')
        ADMIN = 'ADMIN', _('Admin')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    email = models.EmailField(_('email address'), unique=True)

    # Use email for login instead of username if desired, 
    # but for now we'll stick to username for simplicity or follow standard
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
