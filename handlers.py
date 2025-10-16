# handlers.py (root-level shim)
# Makes 'import handlers' work by forwarding to project.handlers (preferred),
# or bot.handlers (fallback).

try:
    from project.handlers import *  # type: ignore
except ModuleNotFoundError:
    try:
        from bot.handlers import *  # type: ignore
    except ModuleNotFoundError as e:
        # Give a clear error so logs are readable
        raise ModuleNotFoundError(
            "Не найден модуль handlers: ни project.handlers, ни bot.handlers. "
            "Создай project/handlers.py (или пакет) и определи нужные классы/функции."
        ) from e
