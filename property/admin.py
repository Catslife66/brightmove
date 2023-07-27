from django.contrib import admin

from .models import Address, PropertyFeature, PropertyPrice, Property, PropertyImage, PropertyWishList


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ['property_object', 'for_sale', 'is_active', 'added_at', 'updated_at']


class PropertyPriceAdmin(admin.ModelAdmin):
    list_display = ['property', 'price_type', 'price', 'added_at', 'updated_at']


admin.site.register(Address)
admin.site.register(PropertyFeature)
admin.site.register(PropertyPrice, PropertyPriceAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyWishList)
