# Sender

## Описание

Telegram-бот для приветствия и общения с новыми участниками канала.

## Технологии

Aiogram, Pyrogram, PostgreSQL, SQLAlchemy, docker, dependency-injector

## Как запустить

Создать .env файл в корне проекта вида:

```env
PROJECT_NAME=telegram_sender
PROJECT_SLUG=sender

POSTGRES_SERVER=app_db

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_DB=tsender

PYTHON_ENV=development

BOT_TOKEN=<ваш токен бота>

GROUP=<ваш канал>

BOT_ID=<id бота>

ADMIN_ID=<id админа>
```

В директории app/app создать файл cred.json и записать туда данные ваших telegram аккаунтов:

```json
{
"1": {
"phone": "<номер>",
"api_id": "<ваш api id>",
"api_hash": "<ваш api hash>"
},

"2": {
"phone": "<номер>",
"api_id": "<ваш api id>",
"api_hash": "<ваш api hash>"
},
}
```

Из корневой директории запустить docker-compose

```bash
docker-compose up -d
```

При первом запуске требуется создать сессии Pyrogram, идём в контейнер

```bash
docker exec -it sender_app bash
```

Переходим в директорию app/app и запускаем скрипт

```bash
cd app/app
python start.py
```

Бот настраивается по команде /settings, доступны следующие опции:

1. Изменение приветственного сообщения
2. Настройка задержки перед приветствием
3. Лимит диалогов на один канал(для избежания блокировки)
