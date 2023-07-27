from django.conf import settings
from django.contrib import admin
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from property.models import Property, PropertyWishList


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_sender')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='notification_recipient')
    timestamp = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)


    @admin.display
    def notification_object(self):
        return f"notification object({self.pk})"


@receiver(post_save, sender=PropertyWishList)
def send_liked_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.property.owner
        liker = instance.user
        liked_property = instance.property
        message = f"Someone liked your property: {liked_property}"
        notification = Notification.objects.create(sender=liker, recipient=recipient, property=liked_property, message=message)