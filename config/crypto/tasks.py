import asyncio
import websockets
import json
from channels.layers import get_channel_layer
from .models import CryptoPrice


async def binance_ws_stream():
    """
    Запускает WebSocket-подключение к Binance и получает обновления цен в реальном времени.

    - Подключается к Binance WebSocket API.
    - Получает данные о торговых операциях (текущая цена BTC/USDT).
    - Сохраняет полученные данные в базе данных (модель CryptoPrice).
    - Отправляет обновления клиентам через Django Channels.

    Логика работы:
    1. Открывает WebSocket-соединение с Binance по заданному URL.
    2. Получает сообщения с актуальной ценой BTC/USDT.
    3. Парсит JSON-ответ, извлекает цену.
    4. Сохраняет цену в базу данных.
    5. Рассылает обновления всем клиентам, подписанным на группу "crypto_updates".
    """

    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    async with websockets.connect(url) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            price = data['p']

            CryptoPrice.objects.create(symbol='BTC/USDT', price=price)

            channel_layer = get_channel_layer()
            await channel_layer.group_send('crypto_updates', {
                'type': 'send_price_update',
                'symbol': 'BTC/USDT',
                'price': price
            })


asyncio.run(binance_ws_stream())

