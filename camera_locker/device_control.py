import subprocess
from .logger import logger
from .config import load_config, save_config

def get_camera_device_ids():
    try:
        cmd = [
            "powershell",
            "-Command",
            "Get-PnpDevice -Class Camera | Select-Object -ExpandProperty InstanceId"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if ids:
            logger.info("Знайдено камери через PowerShell: %s", ids)
        return ids
    except Exception as e:
        logger.warning("Не вдалося отримати DeviceID через PowerShell: %s", e)
        return []

def get_camera_ids_pnputil():
    try:
        cmd = ["pnputil", "/enum-devices", "/class", "Camera"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        ids = []
        for line in result.stdout.splitlines():
            if "Instance ID" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    ids.append(parts[1].strip())
        if ids:
            logger.info("Знайдено камери через pnputil: %s", ids)
        return ids
    except Exception as e:
        logger.error("Помилка отримання DeviceID через pnputil: %s", e)
        return []

def get_or_store_camera_id():
    """
    Повертає DeviceID камери. Якщо його немає в конфігу — знаходить і зберігає.
    """
    cfg = load_config()
    if cfg.get("camera_device_id"):
        return cfg["camera_device_id"]

    ids = get_camera_device_ids()
    if not ids:
        ids = get_camera_ids_pnputil()

    if ids:
        cfg["camera_device_id"] = ids[0]
        save_config(cfg)
        logger.info("DeviceID камери збережено у конфіг: %s", ids[0])
        return ids[0]

    return None

def disable_camera(device_id: str):
    try:
        cmd = [
            "powershell",
            "-Command",
            f'Disable-PnpDevice -InstanceId "{device_id}" -Confirm:$false'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info("Камеру вимкнено (%s).", device_id)
    except Exception as e:
        logger.error("Помилка вимкнення камери: %s", e)

def enable_camera(device_id: str):
    try:
        cmd = [
            "powershell",
            "-Command",
            f'Enable-PnpDevice -InstanceId "{device_id}" -Confirm:$false'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info("Камеру увімкнено (%s).", device_id)
    except Exception as e:
        logger.error("Помилка увімкнення камери: %s", e)