import subprocess
from .logger import log_info, log_error

# Словник для відстеження стану камер
camera_states = {}

def list_cameras():
    """
    Отримує список камер через PowerShell (InstanceId),
    незалежно від того, чи вони увімкнені чи вимкнені.
    """
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-PnpDevice | Where-Object { $_.Class -eq 'Camera' } | Select-Object -ExpandProperty InstanceId"],
            capture_output=True, text=True
        )
        cams = result.stdout.strip().splitlines()
        return cams if cams else []
    except Exception as e:
        log_error(f"Помилка отримання списку камер: {e}")
        return []

def create_guard_and_start():
    """Запускає моніторинг камер і показує їх ID."""
    cams = list_cameras()
    if cams:
        print("Camera Guard запущено. Доступні камери:", cams)
        for cam in cams:
            camera_states[cam] = True
        log_info(f"Camera Guard запущено. Доступні камери: {cams}")
    else:
        print("Камери не знайдено.")
        log_info("Camera Guard запущено. Камери не знайдено.")

def disable_camera(camera_id):
    """Блокує камеру за InstanceId або всі."""
    if camera_id == "all":
        for cam in list_cameras():
            _disable_camera_by_id(cam)
    else:
        _disable_camera_by_id(camera_id)

def enable_camera(camera_id):
    """Розблоковує камеру за InstanceId або всі."""
    if camera_id == "all":
        for cam in list_cameras():
            _enable_camera_by_id(cam)
    else:
        _enable_camera_by_id(camera_id)

def _disable_camera_by_id(cam_id):
    try:
        subprocess.run(
            ["powershell", "-Command",
             f"Disable-PnpDevice -InstanceId '{cam_id}' -Confirm:$false"],
            check=True
        )
        camera_states[cam_id] = False
        print(f"Камеру {cam_id} заблоковано.")
        log_info(f"Камеру {cam_id} заблоковано.")
    except subprocess.CalledProcessError as e:
        print(f"Не вдалося заблокувати камеру {cam_id}.")
        log_error(f"Помилка блокування камери {cam_id}: {e}")

def _enable_camera_by_id(cam_id):
    try:
        for attempt in range(3):  # пробуємо кілька разів
            subprocess.run(
                ["powershell", "-Command",
                 f"Enable-PnpDevice -InstanceId '{cam_id}' -Confirm:$false"],
                check=True
            )

            # перевіряємо статус
            result = subprocess.run(
                ["powershell", "-Command",
                 f"(Get-PnpDevice -InstanceId '{cam_id}').Status"],
                capture_output=True, text=True
            )
            status = result.stdout.strip()
            if status.lower() == "ok":
                camera_states[cam_id] = True
                print(f"Камеру {cam_id} розблоковано.")
                log_info(f"Камеру {cam_id} розблоковано.")
                return

        print(f"Не вдалося розблокувати камеру {cam_id}.")
        log_error(f"Камера {cam_id} лишається вимкненою після спроб розблокування.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка розблокування камери {cam_id}.")
        log_error(f"Помилка розблокування камери {cam_id}: {e}")

def is_camera_enabled(camera_id):
    """Перевіряє, чи камера увімкнена."""
    return camera_states.get(camera_id, True)