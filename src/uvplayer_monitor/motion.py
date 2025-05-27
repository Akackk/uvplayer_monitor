import time
import pyautogui
from PIL import ImageChops

def detect_motion():
    screen_width, screen_height = pyautogui.size()
    region = (0, 0, screen_width, (2 * screen_height) // 3)
    try:
        screenshot1 = pyautogui.screenshot(region=region)
        time.sleep(1)
        screenshot2 = pyautogui.screenshot(region=region)
    except OSError:
        return False
    diff = ImageChops.difference(screenshot1, screenshot2)
    return bool(diff.getbbox())
