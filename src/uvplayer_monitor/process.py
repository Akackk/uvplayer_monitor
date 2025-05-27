import os
import psutil
import ctypes
import time

def kill_uvplayer_processes():
    """Вбиває всі процеси UVPlayer та пов'язані: uvplayer, crashpad, chrome."""
    killed = False
    targets = []

    for proc in psutil.process_iter(['name', 'pid', 'cmdline']):
        try:
            name = proc.info['name'] or ''
            cmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            if any(term in name.lower() or term in cmd.lower()
                   for term in ['uvplayer', 'crashpad', 'chrome']):
                targets.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    for proc in targets:
        try:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                proc.kill()
            killed = True
        except Exception:
            pass

    time.sleep(1)  # Дати ОС оновити трей

    # Примусове оновлення іконок
    ctypes.windll.shell32.SHChangeNotify(0x8000000, 0x1000, None, None)

    return killed

def find_uvplayer_shortcuts():
    """Повертає список ярликів UVPlayer з робочого столу."""
    user_desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    uvplayer_shortcuts = []
    for file in os.listdir(user_desktop):
        if file.lower().endswith(".lnk") and "uvplayer" in file.lower():
            uvplayer_shortcuts.append(os.path.join(user_desktop, file))
    return uvplayer_shortcuts

def count_uvplayer_processes():
    """Підраховує кількість активних процесів, пов’язаних із uvplayer."""
    count = 0
    for p in psutil.process_iter(['name', 'cmdline']):
        try:
            name = p.info['name'] or ''
            cmd = ' '.join(p.info['cmdline']) if p.info['cmdline'] else ''
            if any(term in name.lower() or term in cmd.lower()
                   for term in ['uvplayer', 'crashpad', 'chrome']):
                count += 1
        except Exception:
            pass
    return count
