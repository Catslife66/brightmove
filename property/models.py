from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class PropertyQuerySet(models.QuerySet):
    def filter_by_location(self, location):
        return self.filter(property_address__town__iexact=location)


class PropertySearchManger(models.Manager):
    def get_queryset(self):
        return PropertyQuerySet(self.model, using=self._db)
    
    def filter_by_loaction(self, location):
        return self.get_queryset().filter_by_location(location)


class Property(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_property')
    description = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    for_sale = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)

    objects = models.Manager()
    location = PropertySearchManger()

    class Meta:
        verbose_name_plural = 'properties'


class Address(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='property_address')
    line_1 = models.CharField(max_length=120)
    line_2 = models.CharField(max_length=120, blank=True, null=True)
    town = models.CharField(max_length=50)
    region = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        if self.line_2 is not None:
            if self.region is not None:
                return f"{self.line_1}, {self.line_2}, {self.town}, {self.region}, {self.postcode}"
            return f"{self.line_1}, {self.line_2}, {self.town}, {self.postcode}"
        else:
            if self.region is not None:
                return f"{self.line_1}, {self.town}, {self.region}, {self.postcode}"
            return f"{self.line_1}, {self.town}, {self.postcode}"
    

    def save(self, *args, **kwargs):
        formated_postcode = self.postcode.upper().replace(" ", "")
        formated_postcode = formated_postcode[:3] + " " + formated_postcode[3: ]
        super().save(*args, **kwargs)


class PropertyFeature(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='property_feature')
    PROPERTY_TYPE_CHOICES = [
        ('Detached', 'Detached'),
        ('Semi-detached', 'Semi-detached'),
        ('Flat', 'Flat'),
        ('Bangalow', 'Bangalow')
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    bedroom = models.IntegerField()
    toilet = models.IntegerField()


class PropertyPrice(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='property_price')
    PRICE_TYPE_CHOICES = [
        ('Offers over', 'Offers over'),
        ('Fixed price', 'Fixed price')
    ]
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='Offers over')
    price = models.BigIntegerField()
    added_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property/')
    is_feature = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # only one feature image can be set
        if self.is_feature:
            PropertyImage.objects.filter(property=self.property).update(is_feature=False)
        super().save(*args, **kwargs)


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


class PropertyWishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_property')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='wishlist')
    added_at = models.DateField(auto_now_add=True)


class LocationSearchTracking(models.Model):
    location = models.CharField(max_length=100)
    search_count = models.PositiveIntegerField(default=0)

    def increment_count(self):
        self.search_count += 1
        self.save()