import hashlib


def hash_password(password: str) -> str:
    """Выполняет хеширование пароля"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
