# Структура проекта

## Корневые файлы

### Основные
- `main.py` - Точка входа Telegram бота
- `postgres_db.py` - Менеджер базы данных PostgreSQL
- `config.py` - Конфигурация проекта
- `requirements.txt` - Python зависимости
- `.env` - Переменные окружения (не в git)
- `.gitignore` - Игнорируемые файлы

### Документация
- `README.md` - Основная документация
- `QUICKSTART.md` - Быстрый старт
- `PROJECT_STRUCTURE.md` - Этот файл

### Деплой
- `Procfile` - Конфигурация для Heroku/Render
- `render.yaml` - Конфигурация Render.com

## Модули бота

### Основные обработчики
- `handlers.py` - Обработчики команд и сообщений бота
- `keyboards.py` - Клавиатуры бота
- `admin.py` - Административные команды

### Бизнес-логика
- `payments.py` - Обработка платежей
- `logistics.py` - Управление доставкой
- `promotions.py` - Промокоды и акции
- `crm.py` - CRM функции
- `inventory_management.py` - Управление складом
- `financial_reports.py` - Финансовая отчетность

### Вспомогательные
- `notifications.py` - Отправка уведомлений
- `scheduled_posts.py` - Отложенные публикации
- `analytics.py` - Аналитика
- `security.py` - Безопасность
- `localization.py` - Локализация
- `webhooks.py` - Webhook обработчики
- `marketing_automation.py` - Маркетинговая автоматизация
- `ai_features.py` - AI функции
- `utils.py` - Утилиты
- `logger.py` - Логирование

### Запуск
- `run_bot.py` - Альтернативный запуск бота
- `run_web.py` - Альтернативный запуск веб-панели

## Папки

### database/
SQL скрипты для инициализации базы данных:
- `init_render_db.sql` - Полная схема БД PostgreSQL

### docs/
Документация проекта:
- `README.md` - Подробная документация
- `RENDER_POSTGRES_MIGRATION.md` - Инструкция по миграции

### tests/
Тесты и проверки:
- `test_render_db.py` - Тест подключения к БД
- `test_bot.py` - Тесты бота
- `health_check.py` - Мониторинг здоровья

### web_admin/
Веб-панель администратора (Flask):

**Python файлы:**
- `app.py` - Основное Flask приложение
- `run.py` - Запуск веб-сервера
- `bot_integration.py` - Интеграция с ботом
- `requirements.txt` - Зависимости веб-панели

**HTML шаблоны (templates/):**
- `base.html` - Базовый шаблон
- `login.html` - Страница входа
- `dashboard.html` - Главная панель
- `categories.html` - Управление категориями
- `add_category.html` - Добавление категории
- `products.html` - Управление товарами
- `add_product.html` - Добавление товара
- `edit_product.html` - Редактирование товара
- `orders.html` - Заказы
- `order_detail.html` - Детали заказа
- `customers.html` - Клиенты
- `customer_profile.html` - Профиль клиента
- `analytics.html` - Аналитика
- `financial.html` - Финансы
- `report_profit.html` - Отчет о прибыли
- `inventory.html` - Склад
- `crm.html` - CRM
- `scheduled_posts.html` - Отложенные публикации
- `create_post.html` - Создание поста
- `edit_post.html` - Редактирование поста
- `users.html` - Пользователи

## База данных (PostgreSQL)

### Основные таблицы:
- `users` - Пользователи бота
- `categories` - Категории товаров
- `subcategories` - Подкатегории
- `products` - Товары
- `product_images` - Изображения товаров
- `cart` - Корзина покупок
- `orders` - Заказы
- `order_items` - Позиции заказов
- `reviews` - Отзывы
- `favorites` - Избранное
- `notifications` - Уведомления
- `loyalty_points` - Баллы лояльности
- `promo_codes` - Промокоды
- `promo_uses` - Использование промокодов
- `shipments` - Доставки
- `scheduled_posts` - Отложенные посты
- `post_statistics` - Статистика постов
- `user_activity_logs` - Логи активности

## Переменные окружения (.env)

### Обязательные:
```env
DATABASE_URL=postgresql://...
TELEGRAM_BOT_TOKEN=...
POST_CHANNEL_ID=...
ADMIN_TELEGRAM_ID=...
ADMIN_NAME=...
```

### Опциональные:
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
REDIS_ENABLED=false
SENTRY_DSN=...
```

## Команды запуска

### Локально:
```bash
# Telegram бот
python main.py

# Веб-панель
cd web_admin && python run.py
```

### Тестирование:
```bash
# Проверка БД
python tests/test_render_db.py

# Тест бота
python tests/test_bot.py
```

## Зависимости

### Основные (requirements.txt):
- `python-telegram-bot==21.5` - Telegram Bot API
- `psycopg2-binary==2.9.9` - PostgreSQL драйвер
- `flask==2.3.3` - Веб-фреймворк
- `gunicorn==21.2.0` - WSGI сервер
- `python-dotenv==1.0.0` - Переменные окружения
- `requests==2.31.0` - HTTP клиент

### Дополнительные:
- `psutil==5.9.6` - Мониторинг системы
- `sentry-sdk==1.38.0` - Отслеживание ошибок
- `cryptography==41.0.7` - Шифрование
- `redis==5.0.1` - Кеширование (опционально)

## Архитектура

```
┌─────────────────┐
│  Telegram Bot   │
│    (main.py)    │
└────────┬────────┘
         │
         ├──> handlers.py (команды)
         ├──> keyboards.py (UI)
         ├──> payments.py (платежи)
         ├──> logistics.py (доставка)
         └──> crm.py (CRM)

┌─────────────────┐
│   Web Admin     │
│   (Flask app)   │
└────────┬────────┘
         │
         └──> bot_integration.py

         ┌──────────────┐
         │  PostgreSQL  │
         │   Database   │
         └──────────────┘
```

## Workflow разработки

1. Клонировать репозиторий
2. Установить зависимости: `pip install -r requirements.txt`
3. Настроить `.env`
4. Инициализировать БД: `psql $DATABASE_URL < database/init_render_db.sql`
5. Запустить тесты: `python tests/test_render_db.py`
6. Запустить бота: `python main.py`
7. Запустить веб-панель: `cd web_admin && python run.py`

## Деплой на Render.com

1. Создать PostgreSQL базу
2. Создать Web Service для бота
3. Создать Web Service для админки
4. Настроить переменные окружения
5. Инициализировать БД через `psql`

Подробнее: `docs/RENDER_POSTGRES_MIGRATION.md`
