import json

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.shortcuts import render

from .models import Notification


def notification_count(request):
    recipient = request.user
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        updatechecked = data.get('updatechecked')
        updatechecked = parse_datetime(updatechecked)
        unchecked_notifications = Notification.objects.filter(recipient=recipient, is_read=False, is_checked=False, timestamp__lte=updatechecked)
        unchecked_count = unchecked_notifications.count()
        unchecked_notifications.update(is_checked=True)
    else:
        unchecked_notifications = Notification.objects.filter(recipient=recipient, is_read=False, is_checked=False)
        unchecked_count = unchecked_notifications.count()
    response = {'unchecked_count': unchecked_count}
    return JsonResponse(response)

    
def show_notification_list(request):
    recipient = request.user
    notification_list = Notification.objects.filter(recipient=recipient)

    return render(request, 'notification/partials/notification-list.html', {'obj_list': notification_list})


def read_notification(request, msg_pk):
    msg = Notification.objects.get(pk=msg_pk)
    msg.is_read = True
    msg.save()
    pass