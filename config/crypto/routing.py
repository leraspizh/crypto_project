from django.urls import re_path
from .consumers import BinanceConsumer

websocket_urlpatterns = [
    re_path(r"^ws/crypto/$", BinanceConsumer.as_asgi()),
]

