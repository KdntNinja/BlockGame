from config import Config

from screeninfo import get_monitors

def get_screen_resolution():
    config = Config()
    if config.get("fullscreen") == 1:
        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height
    else:
        screen_width, screen_height = 1600, 800
    return screen_width, screen_height