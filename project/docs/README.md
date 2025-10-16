# Telegram Shop Bot 🛍️

Полнофункциональный бот для интернет-магазина в Telegram с веб-админкой, CRM, аналитикой и автоматизацией.

## ✨ Возможности

### 🤖 Telegram Бот
- Каталог товаров с категориями и подкатегориями
- Корзина и оформление заказов
- Избранное и отзывы
- Программа лояльности и промокоды
- Отслеживание доставки
- Уведомления о статусе заказа
- AI-рекомендации товаров
- Автоматические посты в канал

### 🌐 Web Админ-панель
- Dashboard с метриками и графиками
- Управление товарами и категориями
- Обработка заказов
- CRM и база клиентов
- Аналитика продаж
- Финансовые отчёты
- Управление складом
- Создание автопостов
- Промокоды и акции

### 📊 Аналитика и CRM
- Сегментация клиентов (новые, активные, VIP)
- Анализ поведения пользователей
- Воронка продаж
- Прогнозирование повторных покупок
- RFM-анализ
- Customer Lifetime Value (CLV)
- Отчёты по прибыли и расходам

### 🚀 Автоматизация
- Планировщик постов (утро/день/вечер)
- Уведомления о брошенной корзине
- Автоматические заказы у поставщиков
- Email/SMS рассылки
- Реактивация неактивных клиентов

## 🏗️ Технологии

- **Backend**: Python 3.8+
- **Bot**: Telegram REST API (urllib)
- **Web**: Flask + Gunicorn
- **Database**: Supabase Postgres (33 таблицы)
- **Auth**: JWT + RLS политики
- **Logging**: Rotating file logs
- **Monitoring**: Health checks, Sentry

## 📦 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <your-repo>
cd project
```

### 2. Установите зависимости

```bash
# Проверьте Python и pip
python3 --version  # Нужен 3.8+
pip3 --version

# Установите пакеты
pip3 install -r requirements.txt

# Проверьте установку
python3 -c "from supabase import create_client; print('✅ Supabase OK')"
```

**Получаете ошибку ImportError?** См. [QUICKSTART.md](QUICKSTART.md) или [INSTALL.md](INSTALL.md)

### 3. Настройте переменные окружения

Скопируйте `.env.example` в `.env` и заполните:

```env
# Supabase Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABC...
POST_CHANNEL_ID=-1001234567890
ADMIN_TELEGRAM_ID=123456789
ADMIN_NAME=Admin

# Flask Admin
FLASK_SECRET_KEY=random-secret-key
ENVIRONMENT=development
```

### 4. Запустите бота

```bash
python run_bot.py
```

### 5. Запустите админку

```bash
python run_web.py
```

Откройте http://localhost:5000

## 🚀 Деплой

### Render.com (рекомендуется)

**Сервис 1 - Web Admin:**
```
Type: Web Service
Build: pip install -r requirements.txt
Start: gunicorn -w 4 -b 0.0.0.0:$PORT "run_web:app"
```

**Сервис 2 - Telegram Bot:**
```
Type: Background Worker
Build: pip install -r requirements.txt
Start: python run_bot.py
```

Добавьте все переменные окружения из `.env`

### Heroku

```bash
heroku create your-bot
heroku config:set TELEGRAM_BOT_TOKEN=...
# ... остальные переменные
git push heroku main
```

Heroku автоматически использует `Procfile`

## 📚 Документация

- **[SETUP.md](SETUP.md)** - подробная инструкция по настройке
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - гайд по деплою
- **[CHECKLIST.md](CHECKLIST.md)** - чек-лист перед запуском
- **[FINAL_FIXES.md](FINAL_FIXES.md)** - финальные runtime исправления

## 🗂️ Структура проекта

```
project/
├── run_bot.py              # Запуск бота
├── run_web.py              # Запуск веб-админки
├── main.py                 # Основной код бота
├── supabase_db.py          # Менеджер БД
├── config.py               # Конфигурация
├── logger.py               # Логирование
├── handlers.py             # Обработчики команд
├── scheduled_posts.py      # Планировщик постов
├── crm.py                  # CRM функционал
├── analytics.py            # Аналитика
├── financial_reports.py    # Финансовые отчёты
├── inventory_management.py # Управление складом
├── marketing_automation.py # Маркетинг
├── ai_features.py          # AI рекомендации
├── web_admin/             # Flask админ-панель
│   ├── app.py
│   ├── bot_integration.py
│   └── templates/
├── requirements.txt
├── Procfile
└── .env
```

## 🔧 Основные компоненты

### База данных (Supabase Postgres)

33 таблицы с RLS-политиками:
- users, categories, products, orders
- cart, reviews, favorites, notifications
- loyalty_points, promo_codes, shipments
- inventory_rules, marketing_campaigns
- scheduled_posts, analytics logs
- и многое другое

### Безопасность

- ✅ Все секреты через ENV
- ✅ RLS-политики Supabase
- ✅ JWT аутентификация
- ✅ Rate limiting
- ✅ SQL injection protection
- ✅ Encrypted logs

### Логирование

- `bot.log` - основные логи
- `bot_errors.log` - только ошибки
- `logs/security.log` - события безопасности
- Ротация файлов (10MB, 5 бэкапов)

## 🐛 Troubleshooting

### Бот не отвечает
```bash
tail -f bot.log
# Проверьте TELEGRAM_BOT_TOKEN
```

### Ошибки БД
```bash
# Проверьте SUPABASE_URL и SUPABASE_ANON_KEY
# Убедитесь что миграции применены
```

### Автопосты не идут
- Бот должен быть админом в канале
- POST_CHANNEL_ID правильный (-1001234567890)
- Проверьте расписание в админке

## 🤝 Поддержка

При проблемах проверьте:
1. Логи: `tail -f bot.log bot_errors.log`
2. ENV переменные в `.env`
3. Supabase миграции применены
4. RPC функция `exec_sql` создана

## 🎉 Особенности реализации

### ✅ Готово к production
- Нет хардкода секретов
- Нет обрезанного кода
- Единая Supabase БД
- SQLite→Postgres конвертация
- Автосоздание logs/
- Рабочие entry points

### 🔄 SQLite → Postgres
Автоматическая конвертация:
- `date('now', '-7 days')` → `CURRENT_DATE - INTERVAL '7 days'`
- `datetime('now')` → `NOW()`
- `DATE(column)` → `column::date`

### 🎯 Масштабируемость
- Бот: один экземпляр (long-polling)
- Админка: горизонтальное масштабирование (workers)
- БД: автоматическое (Supabase)

---

**Made with ❤️ for Telegram shop automation**
