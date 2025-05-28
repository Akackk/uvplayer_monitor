import os
import time
import pyautogui
from datetime import datetime
from motion import detect_motion
from process import kill_uvplayer_processes, find_uvplayer_shortcuts
from schedule import find_device_file, get_schedule_from_file
from utils import (
    get_today_opencv_dir,
    create_log_file_if_not_exists,
    write_log_entry,
    save_screenshot,
    restart_computer
)

def main():
    device_file = find_device_file()
    if not device_file:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)
        write_log_entry(log_filename, "❌ Не знайдено жодного файлу -device.json.")
        return

    try:
        start_time, end_time = get_schedule_from_file(device_file)
    except ValueError as e:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)
        write_log_entry(log_filename, f"❌ {e}")
        return

    uvplayer_shortcuts = find_uvplayer_shortcuts()
    if not uvplayer_shortcuts:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)
        write_log_entry(log_filename, "⚠️ Ярлики UVPlayer не знайдено на робочому столі.")
        return

    unsuccessful_attempts = 0
    log_filename = create_log_file_if_not_exists(get_today_opencv_dir())

    while True:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)

        current_time = datetime.now().time()
        schedule_start = datetime.strptime(start_time, "%H:%M").time()
        schedule_end = datetime.strptime(end_time, "%H:%M").time()

        if schedule_start <= current_time <= schedule_end:
            motion_detected = detect_motion()

            if not motion_detected:
                write_log_entry(log_filename, "📷 Динаміка: Ні")
                screenshot_path = save_screenshot(get_today_opencv_dir())
                killed = kill_uvplayer_processes()

                if killed:
                    write_log_entry(log_filename, f"🔁 UVPlayer завершено. Перезапуск.")
                    time.sleep(1)

                for shortcut in uvplayer_shortcuts:
                    try:
                        write_log_entry(log_filename, f"▶️ Спроба запуску UVPlayer з ярлика: {shortcut}")
                        os.startfile(shortcut)
                        time.sleep(5)
                    except Exception as ex:
                        write_log_entry(log_filename, f"⚠️ Помилка запуску UVPlayer: {ex}")

                if not detect_motion():
                    unsuccessful_attempts += 1
                else:
                    unsuccessful_attempts = 0

                if unsuccessful_attempts >= 3:
                    write_log_entry(log_filename, "🔁 Три невдалі спроби. Перезавантаження.")
                    restart_computer("UVPlayer завис — три спроби запуску без динаміки")
        else:
            write_log_entry(log_filename, "⏰ Зараз не робочий час UVPlayer. Очікування...")

        time.sleep(10)

if __name__ == "__main__":
    main()
