import json

from settings import CONFIG_FILE
from default_config import Default

class Config:
    def __init__(self):
        self.filename = CONFIG_FILE
        self.config = self.load_config()

    def load_config(self):
        default_config_instance = Default()
        try:
            with open(self.filename, "r") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    config = default_config_instance.get_defaults()
                if not config:
                    config = default_config_instance.get_defaults()
                return config
        except FileNotFoundError:
            return default_config_instance.get_defaults()

    def save_config(self):
        with open(self.filename, "r") as f:
            existing_config = json.load(f)

        existing_config.update(self.config)

        with open(self.filename, "w") as f:
            json.dump(existing_config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()