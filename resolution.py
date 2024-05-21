import ctypes
from config import Config

def get_screen_resolution():
    config = Config()
    if config.get("fullscreen") == 1:
        if "windll" in dir(ctypes):
            user32 = ctypes.windll.user32
            screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            from Xlib import display
            resolution = display.Display().screen().root.get_geometry()
            screen_width, screen_height = resolution.width, resolution.height
        return screen_width, screen_height
    else:
        return 1600, 800