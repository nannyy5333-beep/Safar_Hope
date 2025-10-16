# project/postgres_db.py (optional compatibility layer inside the package)
from __future__ import annotations
from typing import Any, Iterable, Optional, Dict
from .database import execute as _execute, fetchone as _fetchone, fetchall as _fetchall

class PostgresManager:
    def __init__(self) -> None:
        pass

    def execute(self, sql: str, params: Optional[Iterable[Any]] = None) -> None:
        _execute(sql, tuple(params) if params is not None else None)

    def fetchone(self, sql: str, params: Optional[Iterable[Any]] = None) -> Optional[Dict[str, Any]]:
        return _fetchone(sql, tuple(params) if params is not None else None)

    def fetchall(self, sql: str, params: Optional[Iterable[Any]] = None) -> list[Dict[str, Any]]:
        return _fetchall(sql, tuple(params) if params is not None else None)

def execute(sql: str, params: Optional[Iterable[Any]] = None) -> None:
    _execute(sql, tuple(params) if params is not None else None)

def fetchone(sql: str, params: Optional[Iterable[Any]] = None):
    return _fetchone(sql, tuple(params) if params is not None else None)

def fetchall(sql: str, params: Optional[Iterable[Any]] = None):
    return _fetchall(sql, tuple(params) if params is not None else None)

def get_db() -> PostgresManager:
    return PostgresManager()
