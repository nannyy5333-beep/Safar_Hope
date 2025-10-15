"""
Script to create all HTML templates for web admin panel
"""
import os

TEMPLATES_DIR = '/tmp/cc-agent/58510577/project/web_admin/templates'

templates = {
    'login.html': '''{% extends "base.html" %}
{% block title %}Вход{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-4">
        <h2 class="mb-4">Вход в систему</h2>
        <form method="POST">
            <div class="mb-3">
                <input type="password" name="password" class="form-control" placeholder="Пароль" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Войти</button>
        </form>
    </div>
</div>
{% endblock %}''',

    'dashboard.html': '''{% extends "base.html" %}
{% block content %}
<h1>Панель управления</h1>
<div class="row mt-4">
    <div class="col-md-3"><div class="card"><div class="card-body"><h5>Всего заказов</h5><h2>{{ total_orders }}</h2></div></div></div>
    <div class="col-md-3"><div class="card"><div class="card-body"><h5>Товаров</h5><h2>{{ total_products }}</h2></div></div></div>
    <div class="col-md-3"><div class="card"><div class="card-body"><h5>Клиентов</h5><h2>{{ total_customers }}</h2></div></div></div>
    <div class="col-md-3"><div class="card"><div class="card-body"><h5>Выручка</h5><h2>${{ total_revenue }}</h2></div></div></div>
</div>
{% endblock %}''',

    'orders.html': '''{% extends "base.html" %}
{% block content %}
<h1>Заказы</h1>
<table class="table table-striped mt-3">
    <thead><tr><th>№</th><th>Клиент</th><th>Сумма</th><th>Статус</th><th>Дата</th><th></th></tr></thead>
    <tbody>
    {% for order in orders %}
    <tr>
        <td>{{ order.order_number }}</td>
        <td>{{ order.user_name or order.user_id }}</td>
        <td>${{ order.final_amount }}</td>
        <td>{{ order.status }}</td>
        <td>{{ order.created_at }}</td>
        <td><a href="{{ url_for('order_detail', order_id=order.id) }}" class="btn btn-sm btn-primary">Детали</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'order_detail.html': '''{% extends "base.html" %}
{% block content %}
<h1>Заказ #{{ order_data.order_number }}</h1>
<div class="card mt-3">
    <div class="card-body">
        <p><strong>Статус:</strong> {{ order_data.status }}</p>
        <p><strong>Клиент:</strong> {{ order_data.user_name }}</p>
        <p><strong>Телефон:</strong> {{ order_data.shipping_phone }}</p>
        <p><strong>Адрес:</strong> {{ order_data.shipping_address }}</p>
        <p><strong>Сумма:</strong> ${{ order_data.final_amount }}</p>
        <h5 class="mt-3">Товары:</h5>
        <ul>
        {% for item in order_data.items %}
        <li>{{ item.product_name }} x {{ item.quantity }} = ${{ item.subtotal }}</li>
        {% endfor %}
        </ul>
    </div>
</div>
<a href="{{ url_for('orders') }}" class="btn btn-secondary mt-3">Назад</a>
{% endblock %}''',

    'products.html': '''{% extends "base.html" %}
{% block content %}
<h1>Товары <a href="{{ url_for('add_product') }}" class="btn btn-success">Добавить</a></h1>
<table class="table mt-3">
    <thead><tr><th>Название</th><th>Цена</th><th>Остаток</th><th>Категория</th><th></th></tr></thead>
    <tbody>
    {% for product in products %}
    <tr>
        <td>{{ product.name }}</td>
        <td>${{ product.price }}</td>
        <td>{{ product.stock }}</td>
        <td>{{ product.category_name }}</td>
        <td><a href="{{ url_for('edit_product', product_id=product.id) }}" class="btn btn-sm btn-primary">Изменить</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'add_product.html': '''{% extends "base.html" %}
{% block content %}
<h1>Добавить товар</h1>
<form method="POST" class="mt-3">
    <div class="mb-3"><input type="text" name="name" class="form-control" placeholder="Название" required></div>
    <div class="mb-3"><textarea name="description" class="form-control" placeholder="Описание"></textarea></div>
    <div class="mb-3"><input type="number" step="0.01" name="price" class="form-control" placeholder="Цена" required></div>
    <div class="mb-3"><input type="number" name="stock" class="form-control" placeholder="Остаток" value="0"></div>
    <div class="mb-3"><input type="url" name="image_url" class="form-control" placeholder="URL изображения"></div>
    <div class="mb-3">
        <select name="category_id" class="form-control" required>
            <option value="">Выберите категорию</option>
            {% for cat in categories %}<option value="{{ cat.id }}">{{ cat.name }}</option>{% endfor %}
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{{ url_for('products') }}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}''',

    'edit_product.html': '''{% extends "base.html" %}
{% block content %}
<h1>Редактировать товар</h1>
<form method="POST" class="mt-3">
    <div class="mb-3"><input type="text" name="name" class="form-control" value="{{ product.name }}" required></div>
    <div class="mb-3"><textarea name="description" class="form-control">{{ product.description }}</textarea></div>
    <div class="mb-3"><input type="number" step="0.01" name="price" class="form-control" value="{{ product.price }}" required></div>
    <div class="mb-3"><input type="number" name="stock" class="form-control" value="{{ product.stock }}"></div>
    <div class="mb-3"><input type="url" name="image_url" class="form-control" value="{{ product.image_url }}"></div>
    <div class="mb-3">
        <select name="category_id" class="form-control">
            {% for cat in categories %}<option value="{{ cat.id }}" {% if cat.id == product.category_id %}selected{% endif %}>{{ cat.name }}</option>{% endfor %}
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{{ url_for('products') }}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}''',

    'categories.html': '''{% extends "base.html" %}
{% block content %}
<h1>Категории <a href="{{ url_for('add_category') }}" class="btn btn-success">Добавить</a></h1>
<table class="table mt-3">
    <thead><tr><th>Название</th><th>Описание</th><th>Emoji</th><th>Товаров</th></tr></thead>
    <tbody>
    {% for cat in categories %}
    <tr>
        <td>{{ cat.name }}</td>
        <td>{{ cat.description }}</td>
        <td>{{ cat.emoji }}</td>
        <td>{{ cat.product_count or 0 }}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'add_category.html': '''{% extends "base.html" %}
{% block content %}
<h1>Добавить категорию</h1>
<form method="POST" class="mt-3">
    <div class="mb-3"><input type="text" name="name" class="form-control" placeholder="Название" required></div>
    <div class="mb-3"><textarea name="description" class="form-control" placeholder="Описание"></textarea></div>
    <div class="mb-3"><input type="text" name="emoji" class="form-control" placeholder="Emoji (📱)"></div>
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{{ url_for('categories') }}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}''',

    'customers.html': '''{% extends "base.html" %}
{% block content %}
<h1>Клиенты</h1>
<table class="table mt-3">
    <thead><tr><th>ID</th><th>Имя</th><th>Username</th><th>Телефон</th><th>Заказов</th><th></th></tr></thead>
    <tbody>
    {% for customer in customers %}
    <tr>
        <td>{{ customer.telegram_id }}</td>
        <td>{{ customer.first_name }} {{ customer.last_name }}</td>
        <td>@{{ customer.username }}</td>
        <td>{{ customer.phone }}</td>
        <td>{{ customer.order_count or 0 }}</td>
        <td><a href="{{ url_for('customer_profile', telegram_id=customer.telegram_id) }}" class="btn btn-sm btn-primary">Профиль</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'customer_profile.html': '''{% extends "base.html" %}
{% block content %}
<h1>Профиль клиента</h1>
<div class="card mt-3">
    <div class="card-body">
        <p><strong>Имя:</strong> {{ customer.first_name }} {{ customer.last_name }}</p>
        <p><strong>Username:</strong> @{{ customer.username }}</p>
        <p><strong>Телефон:</strong> {{ customer.phone }}</p>
        <p><strong>Telegram ID:</strong> {{ customer.telegram_id }}</p>
        <p><strong>Дата регистрации:</strong> {{ customer.created_at }}</p>
        <h5 class="mt-3">Заказы:</h5>
        <ul>
        {% for order in orders %}
        <li>Заказ #{{ order.order_number }} - ${{ order.final_amount }} - {{ order.status }}</li>
        {% endfor %}
        </ul>
    </div>
</div>
<a href="{{ url_for('customers') }}" class="btn btn-secondary mt-3">Назад</a>
{% endblock %}''',

    'analytics.html': '''{% extends "base.html" %}
{% block content %}
<h1>Аналитика</h1>
<div class="row mt-4">
    <div class="col-md-6"><div class="card"><div class="card-body"><h5>Статистика продаж</h5><p>Всего заказов: {{ orders_count }}</p><p>Выручка: ${{ revenue }}</p></div></div></div>
    <div class="col-md-6"><div class="card"><div class="card-body"><h5>Популярные товары</h5><ul>{% for p in top_products %}<li>{{ p.name }} ({{ p.sales }})</li>{% endfor %}</ul></div></div></div>
</div>
{% endblock %}''',

    'crm.html': '''{% extends "base.html" %}
{% block content %}
<h1>CRM</h1>
<div class="row mt-4">
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Новые клиенты</h5><p>{{ segments.new_customers|length }}</p></div></div></div>
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Активные</h5><p>{{ segments.active_customers|length }}</p></div></div></div>
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Группы риска</h5><p>{{ segments.at_risk|length }}</p></div></div></div>
</div>
{% endblock %}''',

    'scheduled_posts.html': '''{% extends "base.html" %}
{% block content %}
<h1>Отложенные публикации <a href="{{ url_for('create_post') }}" class="btn btn-success">Создать</a></h1>
<table class="table mt-3">
    <thead><tr><th>Текст</th><th>Дата публикации</th><th>Статус</th><th></th></tr></thead>
    <tbody>
    {% for post in posts %}
    <tr>
        <td>{{ post.message_text[:50] }}...</td>
        <td>{{ post.scheduled_time }}</td>
        <td>{{ post.status }}</td>
        <td><a href="{{ url_for('edit_post', post_id=post.id) }}" class="btn btn-sm btn-primary">Изменить</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'create_post.html': '''{% extends "base.html" %}
{% block content %}
<h1>Создать публикацию</h1>
<form method="POST" class="mt-3">
    <div class="mb-3"><textarea name="message_text" class="form-control" rows="5" placeholder="Текст сообщения" required></textarea></div>
    <div class="mb-3"><input type="datetime-local" name="scheduled_time" class="form-control" required></div>
    <div class="mb-3"><input type="url" name="media_url" class="form-control" placeholder="URL медиа (опционально)"></div>
    <div class="mb-3">
        <select name="media_type" class="form-control">
            <option value="">Без медиа</option>
            <option value="photo">Фото</option>
            <option value="video">Видео</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Создать</button>
    <a href="{{ url_for('scheduled_posts') }}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}''',

    'edit_post.html': '''{% extends "base.html" %}
{% block content %}
<h1>Редактировать публикацию</h1>
<form method="POST" class="mt-3">
    <div class="mb-3"><textarea name="message_text" class="form-control" rows="5" required>{{ post.message_text }}</textarea></div>
    <div class="mb-3"><input type="datetime-local" name="scheduled_time" class="form-control" value="{{ post.scheduled_time }}" required></div>
    <div class="mb-3"><input type="url" name="media_url" class="form-control" value="{{ post.media_url }}"></div>
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{{ url_for('scheduled_posts') }}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}''',

    'inventory.html': '''{% extends "base.html" %}
{% block content %}
<h1>Склад</h1>
<table class="table mt-3">
    <thead><tr><th>Товар</th><th>Остаток</th><th>Мин. уровень</th><th>Статус</th></tr></thead>
    <tbody>
    {% for item in stock %}
    <tr class="{% if item.stock < item.min_stock_level %}table-danger{% endif %}">
        <td>{{ item.name }}</td>
        <td>{{ item.stock }}</td>
        <td>{{ item.min_stock_level }}</td>
        <td>{% if item.stock < item.min_stock_level %}Требуется пополнение{% else %}OK{% endif %}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'financial.html': '''{% extends "base.html" %}
{% block content %}
<h1>Финансы</h1>
<div class="row mt-4">
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Выручка</h5><h2>${{ metrics.revenue }}</h2></div></div></div>
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Расходы</h5><h2>${{ metrics.expenses }}</h2></div></div></div>
    <div class="col-md-4"><div class="card"><div class="card-body"><h5>Прибыль</h5><h2>${{ metrics.profit }}</h2></div></div></div>
</div>
<a href="{{ url_for('report_profit') }}" class="btn btn-primary mt-3">Детальный отчет</a>
{% endblock %}''',

    'report_profit.html': '''{% extends "base.html" %}
{% block content %}
<h1>Отчет о прибыли</h1>
<div class="card mt-3">
    <div class="card-body">
        <p><strong>Период:</strong> {{ period }}</p>
        <p><strong>Выручка:</strong> ${{ revenue }}</p>
        <p><strong>Расходы:</strong> ${{ expenses }}</p>
        <p><strong>Прибыль:</strong> ${{ profit }}</p>
        <h5 class="mt-3">По категориям:</h5>
        <table class="table">
            <thead><tr><th>Категория</th><th>Выручка</th><th>Прибыль</th></tr></thead>
            <tbody>
            {% for cat in categories %}
            <tr>
                <td>{{ cat.name }}</td>
                <td>${{ cat.revenue }}</td>
                <td>${{ cat.profit }}</td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
<a href="{{ url_for('financial') }}" class="btn btn-secondary mt-3">Назад</a>
{% endblock %}''',
}

def create_templates():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    for filename, content in templates.items():
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Created: {filename}')
    print(f'\n✅ All {len(templates)} templates created!')

if __name__ == '__main__':
    create_templates()
