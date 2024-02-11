import json
import os


class Config:
    def __init__(self, filename="config.json"):
        self.file_path = "data/"
        self.filename = os.path.join(self.file_path, filename)
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open(self.filename, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()