"""
PostgreSQL database manager for Telegram shop bot using Render PostgreSQL
"""
import os
import logging
import psycopg
import psycopg
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

def _load_env_if_needed():
    """Load .env file if environment variables are not set"""
    if os.getenv('DATABASE_URL'):
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, '.env')

    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value
        print(f"✓ [postgres_db] Loaded .env from: {env_path}")

_load_env_if_needed()

class PostgresManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')

        print(f"[PostgresManager.__init__] DATABASE_URL: {'✓ Found' if self.database_url else '❌ NOT FOUND'}")

        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                self.database_url
            )
            print(f"✓ [PostgresManager] Connection pool created")
        except Exception as e:
            logging.error(f"Failed to create connection pool: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """
        Execute SQL query with PostgreSQL syntax
        Returns: List of dicts for SELECT, affected rows count for INSERT/UPDATE/DELETE
        """
        print(f"=== EXECUTE_QUERY START ===")
        print(f"Query: {query[:200]}")
        print(f"Params: {params}")
        logging.info(f"[execute_query] Query: {query[:100]}...")

        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                    cursor.execute(query, params)

                    query_upper = query.strip().upper()

                    if query_upper.startswith('SELECT') or 'RETURNING' in query_upper:
                        result = cursor.fetchall()
                        result_list = [dict(row) for row in result]
                        print(f"[execute_query] SELECT/RETURNING returned {len(result_list)} rows")
                        logging.info(f"[execute_query] Result: {result_list}")
                        conn.commit()
                        return result_list
                    else:
                        affected_rows = cursor.rowcount
                        conn.commit()
                        print(f"[execute_query] Affected rows: {affected_rows}")
                        logging.info(f"[execute_query] Affected rows: {affected_rows}")
                        return affected_rows

        except Exception as e:
            logging.error(f"Database error: {e}")
            logging.error(f"Query: {query}")
            logging.error(f"Params: {params}")
            raise

    def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Get user by telegram_id"""
        query = "SELECT * FROM users WHERE telegram_id = %s"
        result = self.execute_query(query, (telegram_id,))
        return result[0] if result else None

    def create_user(self, telegram_id: int, username: str = None, first_name: str = None,
                   last_name: str = None, phone: str = None, is_registered: bool = False) -> Dict:
        """Create new user"""
        query = """
            INSERT INTO users (telegram_id, username, first_name, last_name, phone, is_registered)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        result = self.execute_query(
            query,
            (telegram_id, username, first_name, last_name, phone, is_registered)
        )
        return result[0] if result else None

    def update_user(self, telegram_id: int, **kwargs) -> bool:
        """Update user fields"""
        if not kwargs:
            return False

        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE users SET {set_clause} WHERE telegram_id = %s"
        params = tuple(kwargs.values()) + (telegram_id,)

        affected = self.execute_query(query, params, fetch=False)
        return affected > 0

    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        query = "SELECT * FROM categories ORDER BY name"
        return self.execute_query(query)

    def create_category(self, name: str, description: str = None, emoji: str = None) -> Optional[Dict]:
        """Create new category"""
        query = """
            INSERT INTO categories (name, description, emoji)
            VALUES (%s, %s, %s)
            RETURNING *
        """
        result = self.execute_query(query, (name, description, emoji))
        return result[0] if result else None

    def get_products(self, category_id: str = None) -> List[Dict]:
        """Get products, optionally filtered by category"""
        if category_id:
            query = "SELECT * FROM products WHERE category_id = %s ORDER BY name"
            return self.execute_query(query, (category_id,))
        else:
            query = "SELECT * FROM products ORDER BY name"
            return self.execute_query(query)

    def create_product(self, name: str, description: str, price: float,
                      category_id: str, image_url: str = None, stock: int = 0) -> Optional[Dict]:
        """Create new product"""
        query = """
            INSERT INTO products (name, description, price, category_id, image_url, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        result = self.execute_query(
            query,
            (name, description, price, category_id, image_url, stock)
        )
        return result[0] if result else None

    def get_cart(self, user_id: str) -> List[Dict]:
        """Get user's cart items with product details"""
        query = """
            SELECT c.*, p.name, p.description, p.price, p.image_url
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """
        return self.execute_query(query, (user_id,))

    def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1) -> Optional[Dict]:
        """Add product to cart"""
        query = """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, product_id)
            DO UPDATE SET quantity = cart.quantity + EXCLUDED.quantity
            RETURNING *
        """
        result = self.execute_query(query, (user_id, product_id, quantity))
        return result[0] if result else None

    def close(self):
        """Close connection pool"""
        if hasattr(self, 'connection_pool'):
            self.connection_pool.closeall()
            print("✓ [PostgresManager] Connection pool closed")

# Create global instance
_db_instance = None

def get_db() -> PostgresManager:
    """Get or create database manager instance"""
    global _db_instance
    if _db_instance is None:
        print("🔄 Creating PostgresManager...")
        _db_instance = PostgresManager()
        print("✓ PostgresManager created!")
    return _db_instance
