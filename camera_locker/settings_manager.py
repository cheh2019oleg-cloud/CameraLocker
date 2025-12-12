import json
import os
import cv2

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def get_password():
    settings = load_settings()
    return settings.get("password")

def set_password(password: str):
    settings = load_settings()
    settings["password"] = password
    save_settings(settings)

def detect_cameras(max_check: int = 5):
    """Автоматично визначає доступні камери"""
    camera_ids = []
    for i in range(max_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_ids.append(i)
            cap.release()
    return camera_ids

def get_camera_ids():
    settings = load_settings()
    if "camera_ids" not in settings or not settings["camera_ids"]:
        ids = detect_cameras()
        settings["camera_ids"] = ids
        save_settings(settings)
    return settings["camera_ids"]

def set_camera_ids(camera_ids: list):
    settings = load_settings()
    settings["camera_ids"] = camera_ids
    save_settings(settings)