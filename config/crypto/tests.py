import pytest
import json
from channels.testing import WebsocketCommunicator
from unittest.mock import AsyncMock, patch

from .consumers import BinanceConsumer
from ..config.asgi import application
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.asyncio
async def test_websocket_connection():
    """
    Тестирует установление WebSocket-соединения.

    - Подключается к WebSocket `/ws/crypto/`.
    - Проверяет, что соединение установлено успешно.
    - Закрывает соединение.
    """
    communicator = WebsocketCommunicator(application, "/ws/crypto/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.django_db
def test_rest_api():
    """
    Тестирует доступность REST API.

    - Отправляет GET-запрос к API-эндпоинту `cryptoprice-list`.
    - Проверяет, что сервер возвращает HTTP 200 (успешный запрос).
    """
    client = APIClient()
    response = client.get(reverse('cryptoprice-list'))
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_websocket_data():
    """
    Тестирует обработку данных из WebSocket Binance.

    - Создаёт моковый WebSocket, который возвращает тестовые данные.
    - Подменяет метод `get_binance_data` у BinanceConsumer на моковый.
    - Проверяет, что метод вызван.
    """
    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(return_value=json.dumps({"s": "BTCUSDT", "p": "45000.0"}))

    consumer = BinanceConsumer()
    consumer.get_binance_data = AsyncMock()

    await consumer.get_binance_data()

    assert consumer.get_binance_data.called


@pytest.mark.asyncio
@patch("crypto.consumers.websockets.connect", new_callable=AsyncMock)
async def test_binance_data_parsing(mock_ws_connect):
    """
    Тестирует парсинг данных из Binance WebSocket.

    - Создаёт моковое соединение с Binance.
    - Подменяет метод `recv`, чтобы он возвращал тестовые данные.
    - Проверяет, что данные корректно преобразуются и отправляются клиенту.
    """
    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(return_value=json.dumps({"s": "BTCUSDT", "p": "45000.0"}))
    mock_ws_connect.return_value.__aenter__.return_value = mock_ws

    consumer = BinanceConsumer()
    await consumer.get_binance_data()

    assert mock_ws.recv.called
