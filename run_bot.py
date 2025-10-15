import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("runner")

def main():
    # Пытаемся запустить существующий main() твоего бота
    try:
        import main as bot_main
        if hasattr(bot_main, "main"):
            bot_main.main()
            return
    except Exception as e:
        logger.exception("Не удалось импортировать main.py: %s", e)

    # Вариант B: если бот в пакете project или bot
    for modname in ("project.main", "bot.main"):
        try:
            m = __import__(modname, fromlist=["main"])
            if hasattr(m, "main"):
                m.main()
                return
        except Exception:
            pass

    raise SystemExit("Не найден main() для запуска бота. Проверь расположение main.py.")

if __name__ == "__main__":
    main()
