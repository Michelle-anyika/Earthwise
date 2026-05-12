from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from orders.models import Order
from inventory.models import Inventory
from .models import Notification

def notify_user(user, title, message, n_type):
    # Save to database
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=n_type
    )
    
    # Send via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "content": {
                "title": title,
                "message": message,
                "type": n_type
            }
        }
    )

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created: # Update
        title = f"Order #{instance.id} Update"
        message = f"Your order status has been updated to {instance.get_status_display()}."
        notify_user(instance.user, title, message, Notification.Type.ORDER_STATUS)

@receiver(post_save, sender=Inventory)
def stock_alert_notification(sender, instance, **kwargs):
    if instance.is_low_stock:
        # Notify staff/admins
        from django.contrib.auth import get_user_model
        User = get_user_model()
        staff_users = User.objects.filter(role__in=['STAFF', 'ADMIN'])
        
        title = f"Low Stock Alert: {instance.product.name}"
        message = f"Inventory for {instance.product.name} ({instance.source_type}) is low: {instance.quantity_kg}kg remaining."
        
        for staff in staff_users:
            notify_user(staff, title, message, Notification.Type.STOCK_ALERT)
