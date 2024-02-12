import json
import os

from default import Default

class Config:
    def __init__(self, filename="config.json"):
        self.file_path = "data/"
        self.filename = os.path.join(self.file_path, filename)
        self.config = self.load_config()

    def load_config(self):
        default_instance = Default()
        try:
            with open(self.filename, "r") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    config = default_instance.get_defaults()
                if not config:
                    config = default_instance.get_defaults()
                return config
        except FileNotFoundError:
            return default_instance.get_defaults()

    def save_config(self):
        with open(self.filename, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()