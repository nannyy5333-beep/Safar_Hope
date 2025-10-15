# Changelog

## [2.0.0] - 2025-10-14

### 🔄 Переход на Render PostgreSQL

#### Удалено:
- ❌ Supabase интеграция (`supabase_db.py`)
- ❌ Supabase миграции (`supabase/`, `supabase_migrations/`)
- ❌ Supabase SQL файлы
- ❌ Старые документации (12+ дублирующих MD файлов)
- ❌ Тестовые mock модули
- ❌ Локальная SQLite БД (`shop_bot.db`)
- ❌ Логи и кеш (`__pycache__`, `logs/`, `*.log`)

#### Добавлено:
- ✅ PostgreSQL адаптер (`postgres_db.py`)
- ✅ Инициализация БД (`database/init_render_db.sql`)
- ✅ Тесты подключения (`tests/test_render_db.py`)
- ✅ Полная документация:
  - `README.md` - Основная
  - `QUICKSTART.md` - Быстрый старт
  - `PROJECT_STRUCTURE.md` - Структура
  - `docs/RENDER_POSTGRES_MIGRATION.md` - Миграция
- ✅ Правильный `.gitignore`

#### Изменено:
- 🔄 `requirements.txt` - `psycopg2-binary` вместо `supabase`
- 🔄 `config.py` - `DATABASE_URL` вместо Supabase credentials
- 🔄 `main.py` - импорт `PostgresManager`
- 🔄 `web_admin/app.py` - импорт `PostgresManager`
- 🔄 `.env` - только `DATABASE_URL`

### 📁 Новая структура папок

```
project/
├── database/           # SQL схемы
├── docs/              # Документация
├── tests/             # Тесты и проверки
├── web_admin/         # Веб-панель администратора
├── config/            # (зарезервировано)
└── scripts/           # (зарезервировано)
```

### 📊 Статистика

- **Python файлов**: 23
- **Строк кода**: ~12,500
- **HTML шаблонов**: 18
- **SQL файлов**: 1
- **Документация**: 5 файлов

### 🎯 Преимущества новой версии

1. **Чистый проект**: Удалено 20+ лишних файлов
2. **Ясная структура**: Логичное разделение по папкам
3. **Стандартный PostgreSQL**: Больше гибкости, проще отладка
4. **Полная документация**: Все инструкции в одном месте
5. **Готов к деплою**: Конфигурация Render.com включена

### 🔧 Технические детали

#### База данных:
- **Было**: Supabase (PostgreSQL + RLS + Auth)
- **Стало**: Render PostgreSQL (стандартный PostgreSQL)
- **Connection Pool**: psycopg2.pool.SimpleConnectionPool (1-20 соединений)
- **Параметры**: `%s` вместо `?` или `$1`

#### API изменения:
```python
# Было (Supabase):
result = supabase.table('users').select('*').execute()

# Стало (Render PostgreSQL):
result = db.execute_query('SELECT * FROM users')
```

### 📝 Миграция

Для миграции существующих данных из Supabase:

1. Экспорт: `pg_dump <supabase_url> > dump.sql`
2. Очистка от Supabase-специфики
3. Импорт: `psql $DATABASE_URL < dump.sql`

Подробнее: `docs/RENDER_POSTGRES_MIGRATION.md`

### 🚀 Следующие шаги

1. Инициализировать БД: `psql $DATABASE_URL < database/init_render_db.sql`
2. Установить зависимости: `pip install -r requirements.txt`
3. Проверить подключение: `python tests/test_render_db.py`
4. Запустить: `python main.py`

---

## [1.0.0] - Предыдущая версия

- Supabase интеграция
- Множественные документации
- Неорганизованная структура
