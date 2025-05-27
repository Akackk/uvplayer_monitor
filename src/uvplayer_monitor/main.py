from datetime import datetime
import time
import os
import pyautogui
from .motion import detect_motion
from .process import kill_uvplayer_processes, find_uvplayer_shortcuts
from .schedule import find_device_file, get_schedule_from_file
from .utils import ensure_opencv_folder, create_log_file_if_not_exists, write_log_entry, save_screenshot, restart_computer

def main():
    opencv_dir = ensure_opencv_folder()
    log_filename = create_log_file_if_not_exists(opencv_dir)
    write_log_entry(log_filename, "Запуск UVPlayer Monitor.")
    
    device_file = find_device_file()
    if not device_file:
        write_log_entry(log_filename, "Не знайдено жодного файлу -device.json.")
        return
    
    try:
        start_time, end_time = get_schedule_from_file(device_file)
        write_log_entry(log_filename, f"Розклад роботи: {start_time} - {end_time}")
    except ValueError as e:
        write_log_entry(log_filename, str(e))
        return
    
    uvplayer_shortcuts = find_uvplayer_shortcuts()
    if not uvplayer_shortcuts:
        write_log_entry(log_filename, "Ярлики UVPlayer не знайдено на робочому столі.")
        return
    
    unsuccessful_attempts = 0
    
    while True:
        current_time = datetime.now().time()
        schedule_start = datetime.strptime(start_time, "%H:%M").time()
        schedule_end = datetime.strptime(end_time, "%H:%M").time()
        
        if schedule_start <= current_time <= schedule_end:
            motion_detected = detect_motion()
            if not motion_detected:
                if kill_uvplayer_processes():
                    write_log_entry(log_filename, "UVPlayer завершено. Перезапуск. Причина: Відсутність динаміки на екрані.")
                    save_screenshot(opencv_dir)
                for shortcut in uvplayer_shortcuts:
                    os.startfile(shortcut)
                    write_log_entry(log_filename, f"Запуск UVPlayer: {shortcut}")
                    time.sleep(5)
                
                if not detect_motion():
                    unsuccessful_attempts += 1
                else:
                    unsuccessful_attempts = 0
            
            if unsuccessful_attempts >= 3:
                write_log_entry(log_filename, "Три невдалі спроби перезапуску. Перезавантаження системи.")
                save_screenshot(opencv_dir)
                restart_computer(log_filename, "Три невдалі спроби перезапуску UVPlayer")
        else:
            write_log_entry(log_filename, "Зараз не робочий час UVPlayer. Очікування...")
            time.sleep(60)
        
        time.sleep(10)

if __name__ == "__main__":
    main()
