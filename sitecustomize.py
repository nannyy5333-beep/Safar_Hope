# sitecustomize.py
import sys
try:
    import project.postgres_db as _pg
    sys.modules.setdefault("postgres_db", _pg)
except Exception:
    pass
