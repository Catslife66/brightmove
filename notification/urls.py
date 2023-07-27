from django.urls import path

from . import views

app_name = 'notification'
urlpatterns = [
    path('count/', views.notification_count, name='count'),
    path('all/', views.show_notification_list, name='notification-list'),
]