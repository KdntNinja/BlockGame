import json

from settings import CONFIG_FILE


class Default:
    def __init__(self):
        self.name: str = "Player 1"
        self.fullscreen: int = 0
        self.mode: int = 0
        self.world: int = 0

    def get_defaults(self):
        defaults = {
            "name": self.name,
            "fullscreen": self.fullscreen,
            "mode": self.mode,
            "world": self.world,
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(defaults, f, indent=4)
        return defaults
