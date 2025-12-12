import os
import json
from pathlib import Path

APP_NAME = "Camera Locker"
COMPANY = "Hamsters Company"
APP_ID = "com.hamsters.camera-locker"

APPDATA_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "CameraLocker"
CONFIG_FILE = APPDATA_DIR / "config.json"
LOG_FILE = APPDATA_DIR / "camera_locker.log"

DEFAULT_CONFIG = {
    "version": 1,
    "has_password": False,
    "password": None,  # bcrypt-хеш
    "created_at": None,
    "autostart": False,
    "lock_on_start": True,
    "scan_device_limit": 5,
    "ui_minimized": True
}

def ensure_appdata():
    """Створює директорію AppData для застосунку, якщо вона відсутня."""
    APPDATA_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    """Завантажує конфіг. Якщо пошкоджено — робить .bak та створює новий."""
    ensure_appdata()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Дозаповнення значень за замовчуванням
                for k, v in DEFAULT_CONFIG.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            backup = CONFIG_FILE.with_suffix(".bak")
            CONFIG_FILE.replace(backup)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()

def save_config(cfg: dict):
    """Зберігає конфіг у JSON з індентацією."""
    ensure_appdata()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)