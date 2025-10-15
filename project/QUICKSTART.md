# Быстрый старт

## 1. Установка

```bash
pip install -r requirements.txt
```

## 2. Настройка .env

```env
DATABASE_URL=postgresql://user:password@host:port/database
TELEGRAM_BOT_TOKEN=your_bot_token
POST_CHANNEL_ID=@your_channel
ADMIN_TELEGRAM_ID=your_admin_id
ADMIN_NAME=AdminUser
```

## 3. Инициализация БД

```bash
psql $DATABASE_URL < database/init_render_db.sql
```

## 4. Тест подключения

```bash
python tests/test_render_db.py
```

## 5. Запуск бота

```bash
python main.py
```

## 6. Запуск веб-панели

```bash
cd web_admin
python run.py
```

Веб-панель будет доступна по адресу: http://localhost:5000

## Дополнительно

- Документация: `docs/README.md`
- Миграция: `docs/RENDER_POSTGRES_MIGRATION.md`
