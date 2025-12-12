import bcrypt
import os

PASSWORD_FILE = "camera_locker_password.hash"

def is_password_set():
    """Перевіряє, чи пароль вже встановлений."""
    return os.path.exists(PASSWORD_FILE)

def set_password(password: str):
    """Встановлює новий пароль і зберігає його у файлі."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    with open(PASSWORD_FILE, "wb") as f:
        f.write(hashed)

def verify_password(password: str) -> bool:
    """Перевіряє введений пароль проти збереженого хешу."""
    if not is_password_set():
        return False
    with open(PASSWORD_FILE, "rb") as f:
        stored_hash = f.read()
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

def change_password(new_password: str):
    """Змінює пароль на новий."""
    set_password(new_password)