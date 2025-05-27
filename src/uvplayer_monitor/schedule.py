import os
import json

def find_device_file():
    user_roaming_path = os.path.join(os.environ["APPDATA"], "uvplayer")
    device_files = [f for f in os.listdir(user_roaming_path) if f.endswith("-device.json")]
    if device_files:
        return os.path.join(user_roaming_path, device_files[0])
    return None

def recursive_search(data, key1="startTime", key2="endTime"):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == key1 or key == key2:
                return value
            result = recursive_search(value, key1, key2)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = recursive_search(item, key1, key2)
            if result:
                return result
    return None

def get_schedule_from_file(device_file):
    with open(device_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    start_time = recursive_search(data, "startTime")
    end_time = recursive_search(data, "endTime")
    if start_time is None or end_time is None:
        raise ValueError("Файл не містить ключів 'startTime' або 'endTime'.")
    return start_time, end_time
