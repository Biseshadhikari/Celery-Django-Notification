from celery import shared_task
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Creator, Notification

@shared_task
def send_notification_task(creator_id):
    creator = Creator.objects.filter(id=creator_id).first()
    if creator:
        channel_layer = get_channel_layer()
        for subscriber in creator.subscribers.all():
            notification = Notification(user=subscriber, title=f"{creator.user.username} has uploaded a post")
            notification.save()
            notification_count = Notification.objects.filter(user=subscriber, is_seen=False).count()
            
            # Assuming that the subscriber's username is used as the group name
            async_to_sync(channel_layer.group_send)(
                subscriber.username,  # Recommended to use user ID for uniqueness
                {
                    'type': 'notification.message',
                    'message': notification.title,
                    'count': notification_count
                }
            )
