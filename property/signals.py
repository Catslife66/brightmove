from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import PropertyPrice, PropertyImage


@receiver(pre_save, sender=PropertyPrice)
def detect_price_change(sender, instance, **kwargs):
    if instance.pk:
        original_price = sender.objects.get(pk=instance.pk).price
        if original_price < instance.price:
            instance.reduced_active = False
            instance.increased_active = True
        if original_price > instance.price:
            instance.reduced_active = True
            instance.increased_active = False
    

@receiver(post_save, sender=PropertyPrice)
def update_property_instance(sender, instance, **kwargs):
    if instance.pk:
        property_instance = sender.objects.get(pk=instance.pk).property
        property_instance.updated_at = timezone.now()


@receiver(post_save, sender=PropertyImage)
def post_save_property_image(sender, instance, **kwargs):
    feature_img = PropertyImage.objects.filter(property=instance.property, is_feature=True)
    has_feature_img = feature_img.exists()
    if not has_feature_img:
        first_img = PropertyImage.objects.filter(property=instance.property).first()
        first_img.is_feature=True
        first_img.save()
    if has_feature_img and len(feature_img) > 1 :
        first_feature_img = feature_img.first()
        feature_img.exclude(pk=first_feature_img.pk).update(is_feature=False)