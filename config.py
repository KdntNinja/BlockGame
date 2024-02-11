import json


class Config:
    def __init__(self, filename="config.txt"):
        self.filename = filename
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open(self.filename, "w") as f:
            json.dump(self.config, f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
