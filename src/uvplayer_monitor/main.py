import os
import time
import pyautogui
from datetime import datetime

from uvplayer_monitor.motion import detect_motion
from uvplayer_monitor.process import kill_uvplayer_processes, find_uvplayer_shortcuts, count_uvplayer_processes
from uvplayer_monitor.schedule import find_device_file, get_schedule_from_file
from uvplayer_monitor.utils import (
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
        write_log_entry(log_filename, str(e))
        return

    uvplayer_shortcuts = find_uvplayer_shortcuts()
    if not uvplayer_shortcuts:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)
        write_log_entry(log_filename, "⚠️ Ярлики UVPlayer не знайдено на робочому столі.")
        return

    unsuccessful_attempts = 0

    while True:
        opencv_dir = get_today_opencv_dir()
        log_filename = create_log_file_if_not_exists(opencv_dir)

        current_time = datetime.now().time()
        schedule_start = datetime.strptime(start_time, "%H:%M").time()
        schedule_end = datetime.strptime(end_time, "%H:%M").time()

        if schedule_start <= current_time <= schedule_end:
            motion_detected = detect_motion()

            if not motion_detected:
                opencv_dir = get_today_opencv_dir()
                log_filename = create_log_file_if_not_exists(opencv_dir)
                write_log_entry(log_filename, "⛔ Динаміка: Ні")
                screenshot_path = save_screenshot(opencv_dir)
                killed = kill_uvplayer_processes()
                if killed:
                    write_log_entry(log_filename, f"🛑 UVPlayer завершено. Перезапуск. Причина: Відсутність динаміки. Скрин: {screenshot_path}")
                    time.sleep(1)

                for shortcut in uvplayer_shortcuts:
                    write_log_entry(log_filename, f"👉 Спроба запуску UVPlayer з ярлика: {shortcut}")
                    try:
                        os.startfile(shortcut)
                        time.sleep(5)
                    except Exception as e:
                        write_log_entry(log_filename, f"⚠️ Помилка запуску UVPlayer: {e}")
                        continue

                time.sleep(2)
                if not detect_motion():
                    unsuccessful_attempts += 1
                else:
                    unsuccessful_attempts = 0
            else:
                unsuccessful_attempts = 0

            if unsuccessful_attempts >= 3:
                opencv_dir = get_today_opencv_dir()
                log_filename = create_log_file_if_not_exists(opencv_dir)
                write_log_entry(log_filename, "❌ Три невдалі спроби перезапуску. Перезавантаження системи.")
                save_screenshot(opencv_dir)
                restart_computer("Три невдалі спроби перезапуску UVPlayer")
        else:
            opencv_dir = get_today_opencv_dir()
            log_filename = create_log_file_if_not_exists(opencv_dir)
            write_log_entry(log_filename, "🕒 Зараз не робочий час UVPlayer. Очікування...")
            time.sleep(60)

        time.sleep(10)

if __name__ == "__main__":
    main()
