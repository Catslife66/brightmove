from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.query import QuerySet

from account.models import User


class PropertyQuerySet(models.QuerySet):
    def filter_by_location(self, location):
        return self.filter(property_address__town__iexact=location, is_active=True)


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
    is_active = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    objects = models.Manager()
    location = PropertySearchManger()

    class Meta:
        verbose_name_plural = 'properties'

    @admin.display
    def property_object(self):
        return f"property object({self.pk})"
    

    def save(self, *args, **kwargs):
        if self.pk:
            if User.is_superuser:
                super().save(*args, **kwargs)
            else:
                self.is_active = self.__class__.objects.get(pk=self.pk).is_active
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


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
    reduced_active = models.BooleanField(default=False)
    increased_active = models.BooleanField(default=False)
    added_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class RentalPrice(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='rent')
    deposit = models.DecimalField(max_digits=7, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=7, decimal_places=2)
    weekly_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    added_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.weekly_price is None:
            self.weekly_price = round(self.monthly_price / 4)
        super().save( *args, **kwargs)


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