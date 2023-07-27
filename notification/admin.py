from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_object', 'is_read', 'is_checked', 'timestamp']


admin.site.register(Notification, NotificationAdmin)