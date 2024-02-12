import json

class Default:
    def __init__(self):
        self.name: str = "Player 1"
        self.fullscreen: int = 1
        self.mode: int = 1
        self.world: int = 1

    def get_defaults(self):
        defaults = {
            "name": self.name,
            "fullscreen": self.fullscreen,
            "mode": self.mode,
            "world": self.world,
        }
        with open("config.json", "w") as f:
            json.dump(defaults, f, indent=4)
        return defaults