# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from project.celery import send_notification_background

@receiver(post_save, sender=Post)
def NotificationSignal(sender, instance, created, **kwargs):
    if created:
        send_notification_background.delay(instance.creator.user.id)
