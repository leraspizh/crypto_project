import asyncio
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer


class CryptoPriceViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для просмотра данных о ценах криптовалют.

    Позволяет получать список всех записей цен криптовалют,
    отсортированных по убыванию времени (последние записи идут первыми).
    """
    queryset = CryptoPrice.objects.all().order_by("-timestamp")
    serializer_class = CryptoPriceSerializer


def index(request):
    """
    Представление для отображения главной страницы.

    Рендерит шаблон `index.html`, который является основным
    интерфейсом приложения.
    """
    return render(request, "index.html")


async def stream_data(request):
    """
    Асинхронная функция для потоковой передачи данных в ответе HTTP.

    Возвращает `StreamingHttpResponse`, который постоянно отправляет
    данные клиенту через асинхронный генератор.

    :param request: Объект HTTP-запроса
    :return: StreamingHttpResponse с потоковой передачей данных
    """

    async def data_stream():
        """
        Генератор асинхронных данных.

        Каждую секунду передает клиенту новую порцию данных.
        """
        while True:
            yield "Some data\n"  # Имитация стриминга данных
            await asyncio.sleep(1)

    return StreamingHttpResponse(data_stream(), content_type='text/plain')
