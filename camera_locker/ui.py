import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from camera_locker import settings_manager

class MainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Locker")
        self.root.geometry("400x300")

        # Завантажуємо налаштування
        self.settings = settings_manager.load_settings()

        # Перевіряємо пароль
        if "password" not in self.settings or not self.settings["password"]:
            self.settings["password"] = simpledialog.askstring(
                "Пароль", "Введіть пароль для Camera Locker:", show="*"
            )
            settings_manager.set_password(self.settings["password"])

        # Автоматично визначаємо камери
        self.settings["camera_ids"] = settings_manager.get_camera_ids()

        # Статус
        self.status_label = tk.Label(root, text="Camera Locker готовий", bg="lightgray")
        self.status_label.pack(fill="x", pady=5)

        # Кнопки
        self.lock_button = ttk.Button(root, text="🔒 Заблокувати камери", command=self.lock_cameras)
        self.lock_button.pack(pady=10)

        self.unlock_button = ttk.Button(root, text="🔓 Розблокувати камери", command=self.unlock_cameras)
        self.unlock_button.pack(pady=10)

        self.change_password_button = ttk.Button(root, text="Змінити пароль", command=self.change_password)
        self.change_password_button.pack(pady=10)

        self.change_cameras_button = ttk.Button(root, text="Перевизначити камери", command=self.change_cameras)
        self.change_cameras_button.pack(pady=10)

        # Тема
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        ttk.Label(root, text="Тема:").pack(pady=5)
        ttk.OptionMenu(root, self.theme_var, self.theme_var.get(), "light", "dark", "neon", command=self._apply_theme).pack()

        self._apply_theme(self.theme_var.get())

    def lock_cameras(self):
        # Тут логіка блокування камер
        self.status_label.configure(text=f"Камери {self.settings['camera_ids']} заблоковано", bg="red", fg="white")

    def unlock_cameras(self):
        # Тут логіка розблокування камер
        self.status_label.configure(text=f"Камери {self.settings['camera_ids']} розблоковано", bg="green", fg="white")

    def change_password(self):
        new_pass = simpledialog.askstring("Новий пароль", "Введіть новий пароль:", show="*")
        if new_pass:
            settings_manager.set_password(new_pass)
            messagebox.showinfo("Успіх", "Пароль змінено!")

    def change_cameras(self):
        ids = settings_manager.detect_cameras()
        settings_manager.set_camera_ids(ids)
        self.settings["camera_ids"] = ids
        messagebox.showinfo("Успіх", f"Знайдено камери: {ids}")

    def _apply_theme(self, theme):
        if theme == "light":
            self.root.configure(bg="white")
            self.status_label.configure(bg="lightgray", fg="black")
        elif theme == "dark":
            self.root.configure(bg="#2E2E2E")
            self.status_label.configure(bg="#1C1C1C", fg="white")
        elif theme == "neon":
            self.root.configure(bg="#000000")
            self.status_label.configure(bg="#00FF00", fg="black")
        self.settings["theme"] = theme
        settings_manager.save_settings(self.settings)