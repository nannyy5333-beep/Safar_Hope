# run_bot.py
import os, sys, logging, importlib.util, pathlib, re

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("runner")

# 1) Позволяем явно указать точку входа:
# Примеры:
#   BOT_ENTRY=project.main:main        (импорт по модулю)
#   BOT_ENTRY=bot/main.py:main         (импорт по файлу)
ENTRY = os.getenv("BOT_ENTRY", "").strip()

def run_module_path(mod_path: str, func_name: str = "main"):
    spec = importlib.util.spec_from_file_location("bot_entry", mod_path)
    if not spec or not spec.loader:
        raise ImportError(f"Не удалось загрузить модуль из файла: {mod_path}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)  # type: ignore
    if not hasattr(m, func_name):
        raise AttributeError(f"В {mod_path} нет функции {func_name}()")
    log.info("▶️ Запуск %s:%s()", mod_path, func_name)
    return getattr(m, func_name)()

def run_module_name(mod_name: str, func_name: str = "main"):
    m = __import__(mod_name, fromlist=[func_name])
    if not hasattr(m, func_name):
        raise AttributeError(f"В модуле {mod_name} нет функции {func_name}()")
    log.info("▶️ Запуск %s:%s()", mod_name, func_name)
    return getattr(m, func_name)()

def try_env_entry():
    if not ENTRY:
        return False
    try:
        if ":" in ENTRY:
            target, func = ENTRY.split(":", 1)
        else:
            target, func = ENTRY, "main"
        if target.endswith(".py"):
            return run_module_path(target, func) or True
        else:
            return run_module_name(target, func) or True
    except Exception as e:
        log.error("BOT_ENTRY не сработал (%s): %s", ENTRY, e, exc_info=True)
        return False

def looks_like_main(py_path: pathlib.Path) -> bool:
    try:
        txt = py_path.read_text(encoding="utf-8", errors="ignore")
        # грубая эвристика: есть def main(
        return bool(re.search(r"def\s+main\s*\(", txt))
    except Exception:
        return False

def scan_and_run():
    # Игнорируем служебные каталоги
    ignore_dirs = {".git", ".venv", "venv", "__pycache__", "web_admin", "migrations"}
    root = pathlib.Path(".").resolve()
    candidates = []

    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if parts & ignore_dirs:
            continue
        name = p.name.lower()
        if name in {"main.py", "bot.py"} or looks_like_main(p):
            candidates.append(p)

    # Бонус: пытаемся сначала “очевидные” места
    priority = []
    for p in candidates:
        lp = str(p).lower()
        if lp.endswith("/main.py") and ("/project/" in lp or "/bot/" in lp or lp.count("/") <= 2):
            priority.append(p)
    ordered = priority + [p for p in candidates if p not in priority]

    if not ordered:
        raise SystemExit("Не нашли точку входа (main.py). Укажи переменную BOT_ENTRY, напр.: BOT_ENTRY=project.main:main")

    log.info("ℹ️ Найдены кандидаты: %s", ", ".join(map(str, ordered[:5])))
    return run_module_path(str(ordered[0]))

def main():
    # 1) Если BOT_ENTRY задан — используем его
    if try_env_entry():
        return
    # 2) Иначе пробуем стандартные места по модулю
    for mod in ("main", "project.main", "bot.main"):
        try:
            run_module_name(mod)
            return
        except Exception as e:
            log.info("Не подошло %s: %s", mod, e)
    # 3) Полное сканирование проекта
    scan_and_run()

if __name__ == "__main__":
    main()
