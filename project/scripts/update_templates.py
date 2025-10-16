"""
Update all templates with simplified green/white/black design
"""
import os

TEMPLATES_DIR = '/tmp/cc-agent/58510577/project/web_admin/templates'

templates = {
    'dashboard.html': '''{% extends "base.html" %}
{% block content %}
<h1>Панель управления</h1>
<div class="row mt-4 g-4">
    <div class="col-md-3">
        <div class="stat-card">
            <h5>Всего заказов</h5>
            <h2>{{ total_orders }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <h5>Товаров</h5>
            <h2>{{ total_products }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <h5>Клиентов</h5>
            <h2>{{ total_customers }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <h5>Выручка</h5>
            <h2>${{ total_revenue }}</h2>
        </div>
    </div>
</div>
{% endblock %}''',

    'orders.html': '''{% extends "base.html" %}
{% block content %}
<h1>Заказы</h1>
<div class="card mt-4">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>№ Заказа</th>
                    <th>Клиент</th>
                    <th>Сумма</th>
                    <th>Статус</th>
                    <th>Дата</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            {% for order in orders %}
            <tr>
                <td><strong>{{ order.order_number }}</strong></td>
                <td>{{ order.user_name or order.user_id }}</td>
                <td><strong>${{ order.final_amount }}</strong></td>
                <td>{{ order.status }}</td>
                <td>{{ order.created_at }}</td>
                <td><a href="{{ url_for('order_detail', order_id=order.id) }}" class="btn btn-sm btn-primary">Детали</a></td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'products.html': '''{% extends "base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1>Товары</h1>
    <a href="{{ url_for('add_product') }}" class="btn btn-success">+ Добавить товар</a>
</div>
<div class="card mt-4">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Остаток</th>
                    <th>Категория</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            {% for product in products %}
            <tr>
                <td><strong>{{ product.name }}</strong></td>
                <td><strong>${{ product.price }}</strong></td>
                <td>{{ product.stock }}</td>
                <td>{{ product.category_name }}</td>
                <td><a href="{{ url_for('edit_product', product_id=product.id) }}" class="btn btn-sm btn-primary">Изменить</a></td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'add_product.html': '''{% extends "base.html" %}
{% block content %}
<h1>Добавить товар</h1>
<div class="card mt-4">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Название</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Описание</label>
                <textarea name="description" class="form-control" rows="3"></textarea>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Цена</label>
                    <input type="number" step="0.01" name="price" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Остаток</label>
                    <input type="number" name="stock" class="form-control" value="0">
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">URL изображения</label>
                <input type="url" name="image_url" class="form-control">
            </div>
            <div class="mb-3">
                <label class="form-label">Категория</label>
                <select name="category_id" class="form-control" required>
                    <option value="">Выберите категорию</option>
                    {% for cat in categories %}
                    <option value="{{ cat.id }}">{{ cat.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">Сохранить</button>
                <a href="{{ url_for('products') }}" class="btn btn-secondary">Отмена</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}''',

    'categories.html': '''{% extends "base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1>Категории</h1>
    <a href="{{ url_for('add_category') }}" class="btn btn-success">+ Добавить категорию</a>
</div>
<div class="card mt-4">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Описание</th>
                    <th>Emoji</th>
                    <th>Товаров</th>
                </tr>
            </thead>
            <tbody>
            {% for cat in categories %}
            <tr>
                <td><strong>{{ cat.name }}</strong></td>
                <td>{{ cat.description }}</td>
                <td style="font-size: 1.5rem;">{{ cat.emoji }}</td>
                <td>{{ cat.product_count or 0 }}</td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'customers.html': '''{% extends "base.html" %}
{% block content %}
<h1>Клиенты</h1>
<div class="card mt-4">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Username</th>
                    <th>Телефон</th>
                    <th>Заказов</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            {% for customer in customers %}
            <tr>
                <td>{{ customer.telegram_id }}</td>
                <td><strong>{{ customer.first_name }} {{ customer.last_name }}</strong></td>
                <td>@{{ customer.username }}</td>
                <td>{{ customer.phone }}</td>
                <td>{{ customer.order_count or 0 }}</td>
                <td><a href="{{ url_for('customer_profile', telegram_id=customer.telegram_id) }}" class="btn btn-sm btn-primary">Профиль</a></td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'analytics.html': '''{% extends "base.html" %}
{% block content %}
<h1>Аналитика</h1>
<div class="row mt-4 g-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h5>Статистика продаж</h5>
                <p class="mb-2">Всего заказов: <strong>{{ orders_count }}</strong></p>
                <p class="mb-0">Выручка: <strong style="color: var(--primary-green);">${{ revenue }}</strong></p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h5>Популярные товары</h5>
                <ul class="list-unstyled">
                {% for p in top_products %}
                <li class="mb-2">{{ p.name }} <strong>({{ p.sales }})</strong></li>
                {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
}

def update_templates():
    for filename, content in templates.items():
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Updated: {filename}')
    print(f'\n✅ Updated {len(templates)} templates with green/white/black design!')

if __name__ == '__main__':
    update_templates()
