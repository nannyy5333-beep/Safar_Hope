# sitecustomize.py
# Auto-alias legacy module names to package modules when present.
import sys

# postgres_db alias -> project.postgres_db
try:
    import project.postgres_db as _pg
    sys.modules.setdefault("postgres_db", _pg)
except Exception:
    pass

# handlers alias -> project.handlers
try:
    import project.handlers as _handlers
    sys.modules.setdefault("handlers", _handlers)
except Exception:
    pass
