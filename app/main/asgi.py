'''
Setup ASGI server. There is wesocket-routing in application object.websocket
'''
# Python imports
import os

# Django imports
from django.urls import path

# ASGI websocket imports
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# import cusomt views, classes, consumers
from tournament.consumers import (
    GameResultConsumer,
    KnockoutResultConsumer,
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

websocket_urlpatterns = [
    path('ws/group_stage/', GameResultConsumer.as_asgi()),
    path('ws/knockout_stage/', KnockoutResultConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})