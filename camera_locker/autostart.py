import winreg
from .config import APP_ID
from .logger import logger

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

def enable_autostart():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            exe_path = f'"{__import__("sys").executable}" -m CameraLocker'
            winreg.SetValueEx(key, APP_ID, 0, winreg.REG_SZ, exe_path)
        logger.info("Автозапуск увімкнено.")
    except Exception as e:
        logger.error(f"Не вдалося увімкнути автозапуск: {e}")

def disable_autostart():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_ID)
        logger.info("Автозапуск вимкнено.")
    except FileNotFoundError:
        logger.warning("Автозапуск вже вимкнено.")
    except Exception as e:
        logger.error(f"Не вдалося вимкнути автозапуск: {e}")

def is_autostart_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_ID)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Помилка перевірки автозапуску: {e}")
        return False