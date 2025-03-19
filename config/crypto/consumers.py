from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
import json
import websockets
import asyncio

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

last_prices = {
    "BTC/USDT": None,
    "ETH/USDT": None
}


class BinanceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket-консьюмер для получения данных о криптовалютных курсах
    с Binance и передачи их клиентам в режиме реального времени.
    """

    async def connect(self):
        """
        Обрабатывает установление WebSocket-соединения.

        1. Принимает соединение с клиентом.
        2. Добавляет соединение в группу `crypto_updates`, чтобы можно было
           отправлять обновления сразу нескольким клиентам.
        3. Запускает асинхронную задачу для получения данных с Binance.
        """
        await self.accept()
        await self.channel_layer.group_add("crypto_updates", self.channel_name)
        self.binance_task = asyncio.create_task(self.get_binance_data())

    async def disconnect(self, close_code):
        """
        Обрабатывает разрыв WebSocket-соединения.

        1. Удаляет соединение из группы `crypto_updates`.
        2. Отменяет задачу, которая получала данные с Binance.
        """
        await self.channel_layer.group_discard("crypto_updates", self.channel_name)
        if hasattr(self, "binance_task"):
            self.binance_task.cancel()

    async def get_binance_data(self):
        """
        Подключается к WebSocket API Binance, подписывается на обновления
        цен BTC/USDT и ETH/USDT, обрабатывает входящие сообщения и передает
        их клиентам через WebSocket.

        В случае ошибки подключения делает повторную попытку через 5 секунд.
        """
        params = {"method": "SUBSCRIBE", "params": ["btcusdt@trade", "ethusdt@trade"], "id": 1}
        while True:
            try:
                # Устанавливаем WebSocket-соединение с Binance
                async with websockets.connect(BINANCE_WS_URL) as websocket:
                    await websocket.send(json.dumps(params))  # Подписываемся на обновления
                    async for response in websocket:
                        data = json.loads(response)

                        if "s" in data and "p" in data:
                            symbol = data["s"].replace("USDT", "/USDT")  # Приводим символ к формату BTC/USDT
                            try:
                                price = float(data["p"])
                            except ValueError:
                                print(f"Некорректная цена для {symbol}: {data['p']}")
                                continue

                            # Проверяем, изменился ли курс
                            if last_prices.get(symbol) != price:
                                last_prices[symbol] = price
                                timestamp = timezone.now()
                                print(f"Получены данные для {symbol}: {price} на {timestamp}")

                                # Отправляем данные клиентам через WebSocket
                                await self.send_price_update(symbol, price, timestamp)

            except Exception as e:
                print(f"Ошибка WebSocket Binance: {e}")
                await asyncio.sleep(5)  # Ожидание перед повторным подключением

    async def send_price_update(self, symbol, price, timestamp):
        """
        Отправляет обновленные данные о цене криптовалюты клиенту через WebSocket.

        :param symbol: Тикер криптовалютной пары (например, BTC/USDT).
        :param price: Текущая цена криптовалюты.
        :param timestamp: Временная метка обновления.
        """
        try:
            await self.send(text_data=json.dumps({
                "type": "send_price_update",
                "symbol": symbol,
                "price": str(price),  # Преобразуем цену в строку
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }))
        except Exception as e:
            print(f"Ошибка при отправке данных через WebSocket: {e}")

