# Binance WebSocket Django Project

Проект на Django для интеграции с WebSocket API Binance. Используется для получения обновлений цен на криптовалюты в реальном времени и их обработки в приложении.

## Требования

- Python 3.9 или выше
- PostgreSQL (или другой совместимый бэкенд базы данных)
- Redis (для Channels)

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <ссылка-на-репозиторий>
   cd <папка-проекта>
2. **Создайте и активируйте виртуальное окружение:**

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # для macOS/Linux

3. **Установите зависимости:**

   ```bash
    pip install -r requirements.txt

4. **Примените миграции базы данных:**

   ```bash
    python manage.py makemigrations
    python manage.py migrate



## Настройка Redis для Channels
1. **Убедитесь, что Redis установлен и запущен на вашем компьютере. Для macOS можно использовать Homebrew:**

   ```bash
    brew install redis
    redis-server
2. **В файле config/settings.py убедитесь, что параметры CHANNEL_LAYERS настроены на использование Redis:**

   ```bash
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
        },
    }
## Запуск проекта
1. **Запустите сервер с использованием Uvicorn:**

   ```bash
    uvicorn config.asgi:application --reload
2. **Соберите статические файлы: После внесения изменений в статику, соберите статические файлы:**

   ```bash
    python manage.py collectstatic --noinput
## Тестирование
1. **Проект использует pytest для тестирования. Чтобы запустить тесты, выполните:**

   ```bash
    pytest
   
**Тесты включают:**
1. Проверку WebSocket-соединения с Binance.
2. Тестирование API с использованием Django REST Framework.
3. Тестирование обработки данных из WebSocket.

## Структура проекта
1. config/ - настройки проекта Django (ASGI, WSGI, URL-ы).
2. crypto/ - приложение для работы с криптовалютами, обработка данных из WebSocket.
3. templates/ - HTML-шаблоны (index.html).
4. static/ - статические файлы (CSS, JavaScript).
5. tests/ - тесты для WebSocket и API.

## Примечания
1. Убедитесь, что у вас установлен PostgreSQL и Redis.
2. Проверьте настройки переменных окружения и настройки базы данных.
3. Для работы с WebSocket необходимо подключение к Redis, и сервер Redis должен быть запущен на вашем компьютере.
