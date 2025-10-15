# Миграция на Render PostgreSQL

## Что изменено

Проект переключен с **Supabase** на **Render PostgreSQL** - стандартную PostgreSQL базу данных.

### Изменения в коде:

1. **Новый адаптер**: `postgres_db.py` - замена для `supabase_db.py`
2. **Обновлены зависимости**: `psycopg2-binary` вместо `supabase` и `postgrest`
3. **Обновлена конфигурация**: `.env` теперь использует `DATABASE_URL`
4. **Обновлены импорты**:
   - `main.py`: использует `PostgresManager` вместо `SupabaseManager`
   - `web_admin/app.py`: использует `PostgresManager` вместо `SupabaseManager`

## Шаги по развертыванию

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте/обновите файл `.env`:

```env
# Render PostgreSQL Database
DATABASE_URL=postgresql://safar_db_1hxu_user:sAHIfScc0qITaIetKvhHyKltLQMlyXra@dpg-d3n3u6euk2gs73b3rg9g-a.frankfurt-postgres.render.com/safar_db_1hxu

# Telegram Bot
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
POST_CHANNEL_ID=YOUR_CHANNEL_ID_HERE
ADMIN_TELEGRAM_ID=YOUR_ADMIN_ID_HERE
ADMIN_NAME=AdminUser
```

### 3. Инициализация базы данных

Выполните SQL скрипт для создания схемы:

**Способ 1: Используя psql (рекомендуется)**

```bash
psql postgresql://safar_db_1hxu_user:sAHIfScc0qITaIetKvhHyKltLQMlyXra@dpg-d3n3u6euk2gs73b3rg9g-a.frankfurt-postgres.render.com/safar_db_1hxu < init_render_db.sql
```

**Способ 2: Через Render Dashboard**

1. Перейдите в Render Dashboard → Your PostgreSQL Database
2. Откройте вкладку "Query"
3. Скопируйте содержимое `init_render_db.sql`
4. Вставьте и выполните

### 4. Проверка подключения

Запустите тестовый скрипт:

```bash
python test_render_db.py
```

Вы должны увидеть:

```
==================================================
Testing Render PostgreSQL Connection
==================================================

✓ Database connection established!

📊 Testing database query...
✓ Connected to database: safar_db_1hxu
✓ PostgreSQL version: PostgreSQL 16.x...

📋 Checking tables...
✓ Found 23 tables:
  - categories
  - cart
  - favorites
  - ...

==================================================
✓ All tests passed!
==================================================
```

### 5. Запуск проекта

**Локально:**

```bash
# Запуск бота
python main.py

# Запуск веб-админки
cd web_admin
python run.py
```

**На Render.com:**

1. Загрузите все обновленные файлы
2. Убедитесь что `DATABASE_URL` установлен в Environment Variables
3. Render автоматически перезапустит сервис

## Основные отличия от Supabase

### 1. Нет RLS (Row Level Security)

Render PostgreSQL - это стандартная PostgreSQL без Supabase-специфичных фич вроде RLS и auth.uid(). Контроль доступа теперь на уровне приложения.

### 2. Прямые SQL запросы

```python
# Было (Supabase):
result = supabase.table('categories').select('*').execute()

# Стало (Render PostgreSQL):
result = db.execute_query('SELECT * FROM categories')
```

### 3. Нет функции exec_sql

В Render PostgreSQL нет обертки `exec_sql`. Все запросы выполняются напрямую через `psycopg2`.

### 4. Параметры запросов

```python
# PostgreSQL использует %s для параметров:
query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
db.execute_query(query, ('Категория', 'Описание'))
```

## API PostgresManager

### Основные методы:

```python
from postgres_db import get_db

db = get_db()

# Получить пользователя
user = db.get_user(telegram_id=123456)

# Создать пользователя
user = db.create_user(
    telegram_id=123456,
    username='john',
    first_name='John'
)

# Обновить пользователя
db.update_user(telegram_id=123456, phone='+123456789')

# Категории
categories = db.get_categories()
category = db.create_category(name='Электроника', emoji='📱')

# Товары
products = db.get_products(category_id='uuid-here')
product = db.create_product(
    name='iPhone',
    description='...',
    price=999.99,
    category_id='uuid-here',
    stock=10
)

# Корзина
cart_items = db.get_cart(user_id='uuid-here')
db.add_to_cart(user_id='uuid-here', product_id='uuid-here', quantity=2)

# Произвольные запросы
result = db.execute_query('SELECT * FROM orders WHERE user_id = %s', ('uuid-here',))
```

## Миграция данных из Supabase (опционально)

Если нужно перенести данные из старой Supabase БД:

### 1. Экспорт из Supabase

```bash
# Получите connection string из Supabase Dashboard
pg_dump "postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres" > supabase_dump.sql
```

### 2. Импорт в Render

```bash
psql $DATABASE_URL < supabase_dump.sql
```

**Примечание:** Удалите Supabase-специфичные элементы из дампа:
- RLS политики
- auth схемы
- storage схемы

## Troubleshooting

### Ошибка: "psycopg2 module not found"

```bash
pip install psycopg2-binary
```

### Ошибка подключения

Проверьте `DATABASE_URL` в `.env`:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_URL'))"
```

### Таблицы не найдены

Запустите `init_render_db.sql`:

```bash
psql $DATABASE_URL < init_render_db.sql
```

### Медленные запросы

Проверьте индексы:

```sql
-- Посмотреть существующие индексы
SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public';
```

## Преимущества Render PostgreSQL

✅ Стандартная PostgreSQL - больше гибкости
✅ Прямые SQL запросы - полный контроль
✅ Меньше абстракций - проще отладка
✅ Бесплатный tier на Render
✅ Автоматические бэкапы

## Контакты

По вопросам миграции обращайтесь к администратору проекта.
