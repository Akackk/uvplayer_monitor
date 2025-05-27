import os
import psutil
import ctypes
import time

def kill_uvplayer_processes():
    """Завершує всі процеси UVPlayer і оновлює системний трей."""
    killed = False
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and 'uvplayer' in proc.info['name'].lower():
                proc.kill()
                proc.wait(5)  # Дочекатись завершення (до 5 сек)
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Примусово оновити системні іконки (трей)
    ctypes.windll.shell32.SHChangeNotify(0x8000000, 0x1000, None, None)

    # Додаткова перевірка — чи щось лишилось
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] and 'uvplayer' in proc.info['name'].lower():
            print(f"[⚠] Ще активний процес UVPlayer: PID={proc.info['pid']}")

    return killed

def find_uvplayer_shortcuts():
    """Знаходить всі ярлики UVPlayer на робочому столі."""
    user_desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    uvplayer_shortcuts = []
    for file in os.listdir(user_desktop):
        if file.lower().endswith(".lnk") and "uvplayer" in file.lower():
            uvplayer_shortcuts.append(os.path.join(user_desktop, file))
    return uvplayer_shortcuts
