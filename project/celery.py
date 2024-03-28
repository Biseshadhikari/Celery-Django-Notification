import os
from time import sleep
from celery import Celery
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.models import Creator, Notification
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def send_notification_background(post_creator_id):
    user = User.objects.get(pk=post_creator_id)
    creator = Creator.objects.filter(user=user).first()
    
    if creator:
        channel_layer = get_channel_layer()
        for subscriber in creator.subscribers.all():
            notification = Notification(user=subscriber, title=f"{creator} has uploaded a post")
            notification.save()
            notification_count = Notification.objects.filter(user=subscriber, is_seen=False).count()

            # Configure event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run async code within the event loop
            async def send_message():
                await channel_layer.group_send(
                    subscriber.username,
                    {
                        'type': 'chat.message',
                        'message': f"{creator} has uploaded a post",
                        'count': notification_count
                    }
                )
            
            loop.run_until_complete(send_message())