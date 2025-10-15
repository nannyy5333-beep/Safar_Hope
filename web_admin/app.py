import os
from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from project.database import fetchall, fetchone, execute

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

HOME_TMPL = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Safar Admin</title>
    <style>
      body{font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin:0; padding:24px; background:#0b0b0b; color:#fafafa}
      .card{background:#151515; border:1px solid #222; border-radius:16px; padding:20px; margin-bottom:16px}
      .btn{display:inline-block; padding:10px 14px; border-radius:10px; border:1px solid #444; text-decoration:none; color:#fff}
      table{width:100%; border-collapse: collapse}
      th, td{padding:8px 10px; border-bottom: 1px solid #222}
      th{text-align:left; color:#bbb; font-weight:600}
      input, select{background:#101010; color:#fff; border:1px solid #333; border-radius:8px; padding:8px 10px}
      .grid{display:grid; gap:12px; grid-template-columns: repeat(2, minmax(0,1fr))}
      .muted{color:#aaa}
    </style>
  </head>
  <body>
    <div class="card">
      <h2>Safar Web Admin</h2>
      <p class="muted">Подключено к PostgreSQL. Быстрые ссылки:</p>
      <a class="btn" href="{{ url_for('health') }}">/health</a>
      <a class="btn" href="{{ url_for('products') }}">Товары</a>
      <a class="btn" href="{{ url_for('categories') }}">Категории</a>
    </div>

    <div class="card">
      <h3>Сводка</h3>
      <div class="grid">
        <div>
          <div class="muted">Товаров</div>
          <div style="font-size:28px">{{ stats['products'] }}</div>
        </div>
        <div>
          <div class="muted">Категорий</div>
          <div style="font-size:28px">{{ stats['categories'] }}</div>
        </div>
      </div>
    </div>
  </body>
</html>
'''

@app.route("/")
def home():
    products_count = fetchone("select count(*) as c from products")["c"]
    categories_count = fetchone("select count(*) as c from categories")["c"]
    return render_template_string(HOME_TMPL, stats={"products": products_count, "categories": categories_count})

@app.get("/health")
def health():
    try:
        one = fetchone("select 1 as ok")
        return jsonify({"status": "ok", "db": one["ok"] == 1})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.get("/products")
def products():
    rows = fetchall("select id, name, price, stock, created_at from products order by id desc limit 100")
    return jsonify(rows)

@app.post("/products")
def create_product():
    data = request.get_json(force=True)
    name = data.get("name")
    price = data.get("price", 0)
    stock = data.get("stock", 0)
    if not name:
        return jsonify({"error": "name required"}), 400
    execute("insert into products (name, price, stock) values (%s, %s, %s)", (name, price, stock))
    return jsonify({"ok": True})

@app.get("/categories")
def categories():
    rows = fetchall("select id, name from categories order by id")
    return jsonify(rows)

@app.post("/categories")
def create_category():
    data = request.get_json(force=True)
    name = data.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400
    execute("insert into categories (name) values (%s)", (name,))
    return jsonify({"ok": True})
