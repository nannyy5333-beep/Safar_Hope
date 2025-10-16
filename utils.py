# utils.py (root-level shim)
# Makes `from utils import ...` work whether your real code lives in project/utils.py or not.

try:
    # Prefer your real implementation if it exists
    from project.utils import *  # type: ignore
except ModuleNotFoundError:
    # Minimal safe fallbacks (you can replace with your actual logic)
    import re
    def validate_phone(s: str) -> bool:
        if not isinstance(s, str):
            return False
        # Very permissive: digits, +, spaces, (), -
        s2 = re.sub(r"[\s()\-]", "", s)
        return bool(re.fullmatch(r"\+?\d{7,15}", s2))

    def validate_email(s: str) -> bool:
        if not isinstance(s, str):
            return False
        # Simple RFC-ish check
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", s))
