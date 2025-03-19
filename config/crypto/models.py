from django.db import models

class CryptoPrice(models.Model):
    """
    Модель для хранения данных о ценах криптовалют.

    Поля:
    - symbol (CharField): Символ криптовалютной пары (например, 'BTC/USDT').
    - price (DecimalField): Цена криптовалюты с высокой точностью.
    - timestamp (DateTimeField): Временная метка, автоматически устанавливаемая при создании записи.
    """

    symbol = models.CharField(max_length=20, help_text="Символ криптовалютной пары (например, 'BTC/USDT').")
    price = models.DecimalField(max_digits=20, decimal_places=10, help_text="Цена криптовалюты с высокой точностью.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Дата и время фиксации цены.")

    def __str__(self):
        """
        Возвращает строковое представление объекта, удобное для отображения.

        :return: Строка формата '<symbol> - <price> at <timestamp>'.
        """
        return f'{self.symbol} - {self.price} at {self.timestamp}'

