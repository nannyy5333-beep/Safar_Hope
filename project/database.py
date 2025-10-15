import os
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задан. Укажи переменную окружения.")

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10, kwargs={"autocommit": True})

def execute(sql: str, params: tuple | list | None = None):
    with pool.connection() as conn, conn.cursor() as cur:
        cur.execute(sql, params or ())

def fetchone(sql: str, params: tuple | list | None = None):
    with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

def fetchall(sql: str, params: tuple | list | None = None):
    with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()
