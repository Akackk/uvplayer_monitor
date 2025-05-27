import os
import psutil

def kill_uvplayer_processes():
    killed = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'uvplayer' in proc.info['name'].lower():
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return killed

def find_uvplayer_shortcuts():
    user_desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    uvplayer_shortcuts = []
    for file in os.listdir(user_desktop):
        if file.lower().endswith(".lnk") and "uvplayer" in file.lower():
            uvplayer_shortcuts.append(os.path.join(user_desktop, file))
    return uvplayer_shortcuts
