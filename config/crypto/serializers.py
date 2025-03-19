from rest_framework import serializers
from .models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CryptoPrice.

    Позволяет преобразовывать объекты модели в JSON-формат и обратно,
    что необходимо для работы с API.

    Метаданные:
    - model (CryptoPrice): Определяет, что этот сериализатор работает с моделью CryptoPrice.
    - fields ('__all__'): Включает все поля модели в сериализацию. Можно указать конкретные поля при необходимости.
    """

    class Meta:
        model = CryptoPrice
        fields = '__all__'
