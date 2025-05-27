import os
import shutil
from datetime import datetime
import pyautogui

def get_today_opencv_dir():
    """Повертає шлях до директорії OpenCV на сьогодні, створюючи її при потребі."""
    base_dir = r"C:\Users\Public\OpenCV"
    current_date = datetime.now().strftime("%d-%m-%Y")
    date_dir = os.path.join(base_dir, current_date)
    os.makedirs(date_dir, exist_ok=True)
    delete_old_folders(base_dir)
    return date_dir

def create_log_file_if_not_exists(opencv_dir):
    log_filename = os.path.join(opencv_dir, f"log_{datetime.now().strftime('%d-%m-%Y')}.txt")
    if not os.path.exists(log_filename):
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write("")
    return log_filename

def write_log_entry(log_filename, message):
    now = datetime.now()
    current_time_str = now.strftime("%H:%M:%S")
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write(f"{current_time_str} {message}\n")

def save_screenshot(opencv_dir):
    screenshot_name = f"{datetime.now().strftime('%H_%M_%S')}.png"
    screenshot_path = os.path.join(opencv_dir, "screenshots", screenshot_name)
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    pyautogui.screenshot(screenshot_path)
    return screenshot_path

def delete_old_folders(base_dir, max_age_days=62):
    current_time = datetime.now()
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    folders.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)))
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        folder_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
        if (current_time - folder_time).days > max_age_days:
            shutil.rmtree(folder_path)

def restart_computer(log_filename, reason):
    write_log_entry(log_filename, f"Причина перезавантаження: {reason}")
    os.system("shutdown /r /f /t 0")
