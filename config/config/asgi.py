import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.conf.urls.static import static
from crypto.routing import websocket_urlpatterns

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE, если она не задана
if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Инициализируем Django-приложение
django.setup()

"""
ASGI-конфигурация для проекта Django.

Этот файл определяет маршрутизацию для различных типов подключений: HTTP, WebSocket и статических файлов.
"""

application = ProtocolTypeRouter({
    # HTTP-запросы обрабатываются стандартным ASGI-приложением Django.
    # Это позволяет сервировать API, HTML-страницы и другие стандартные веб-запросы.
    "http": get_asgi_application(),

    # WebSocket-соединения маршрутизируются через URLRouter.
    # Используется для обработки WebSocket-запросов, например, для обновления цен криптовалют в реальном времени.
    "websocket": URLRouter(websocket_urlpatterns),

    # Статические файлы (CSS, JS, изображения) обслуживаются через настройки Django.
    # Позволяет раздавать статику при использовании ASGI-сервера.
    "static": static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
})


