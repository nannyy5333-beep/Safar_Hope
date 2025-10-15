# Telegram Shop Bot

Полнофункциональный Telegram бот для интернет-магазина с веб-панелью администратора.

## Возможности

### Для пользователей:
- 🛍 Просмотр каталога товаров по категориям
- 🛒 Корзина покупок
- 📦 Оформление заказов
- 📍 Отправка геолокации для доставки
- 📋 История заказов
- ⭐ Избранные товары
- 💬 Отзывы о товарах
- 🎁 Промокоды и скидки
- 🏆 Программа лояльности

### Для администраторов (веб-панель):
- 📊 Аналитика и статистика
- 📦 Управление товарами и категориями
- 📋 Управление заказами
- 👥 Управление клиентами (CRM)
- 📢 Отложенные публикации в канал
- 💰 Финансовые отчеты
- 📦 Управление складом

## Технологии

- **Язык**: Python 3.9+
- **Telegram API**: python-telegram-bot 21.5
- **База данных**: PostgreSQL (Render)
- **Веб-фреймворк**: Flask
- **Деплой**: Render.com

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd project
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
POST_CHANNEL_ID=@your_channel
ADMIN_TELEGRAM_ID=your_admin_id
ADMIN_NAME=AdminUser
```

### 4. Инициализация базы данных

```bash
psql $DATABASE_URL < database/init_render_db.sql
```

### 5. Запуск

**Telegram бот:**
```bash
python main.py
```

**Веб-панель:**
```bash
cd web_admin
python run.py
```

## Структура проекта

```
project/
├── main.py                 # Точка входа для Telegram бота
├── postgres_db.py          # Менеджер базы данных
├── handlers.py             # Обработчики команд бота
├── keyboards.py            # Клавиатуры бота
├── config.py               # Конфигурация
├── utils.py                # Утилиты
├── logger.py               # Логирование
├── payments.py             # Обработка платежей
├── logistics.py            # Управление доставкой
├── promotions.py           # Промокоды и акции
├── crm.py                  # CRM функции
├── analytics.py            # Аналитика
├── notifications.py        # Уведомления
├── scheduled_posts.py      # Отложенные публикации
├── security.py             # Безопасность
├── localization.py         # Локализация
├── database/
│   └── init_render_db.sql  # Схема БД
├── tests/
│   ├── test_render_db.py   # Тест подключения к БД
│   ├── test_bot.py         # Тесты бота
│   └── health_check.py     # Проверка здоровья
├── docs/
│   ├── README.md           # Документация
│   └── RENDER_POSTGRES_MIGRATION.md
├── web_admin/
│   ├── app.py              # Flask приложение
│   ├── run.py              # Запуск веб-сервера
│   ├── bot_integration.py  # Интеграция с ботом
│   └── templates/          # HTML шаблоны
└── requirements.txt        # Зависимости
```

## Документация

Подробная документация находится в папке `docs/`:

- [Миграция на Render PostgreSQL](docs/RENDER_POSTGRES_MIGRATION.md)
- [API документация](docs/README.md)

## Деплой на Render.com

### 1. Создайте PostgreSQL базу данных

В Render Dashboard:
- New → PostgreSQL
- Скопируйте External Database URL

### 2. Создайте Web Service

В Render Dashboard:
- New → Web Service
- Подключите репозиторий
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`

### 3. Настройте переменные окружения

В Render → Environment:
```
DATABASE_URL=<your_postgres_url>
TELEGRAM_BOT_TOKEN=<your_token>
POST_CHANNEL_ID=<your_channel>
ADMIN_TELEGRAM_ID=<your_id>
```

### 4. Инициализируйте БД

```bash
psql <DATABASE_URL> < database/init_render_db.sql
```

## Тестирование

```bash
# Проверка подключения к БД
python tests/test_render_db.py

# Запуск тестов бота
python tests/test_bot.py
```

## Лицензия

MIT License

## Контакты

По вопросам обращайтесь к администратору проекта.
