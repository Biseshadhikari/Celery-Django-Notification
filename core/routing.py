# core/routing.py

from django.urls import path
from . import consumers

websocket_patterns = [
    path('ws/connect/', consumers.NotificationConsumer.as_asgi()),
]