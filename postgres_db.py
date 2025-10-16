# postgres_db.py (top-level)
# Make legacy 'from postgres_db import ...' work from anywhere.
from project.postgres_db import PostgresManager, get_db, execute, fetchone, fetchall

__all__ = ["PostgresManager", "get_db", "execute", "fetchone", "fetchall"]
