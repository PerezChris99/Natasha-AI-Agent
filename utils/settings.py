import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.settings_file = Path("settings.json")
        self.defaults = {
            "hotkey": "ctrl+space",
            "startup": False,
            "voice_enabled": True,
            "language": "en-US",
            "theme": "light"
        }
        self.load_settings()

    def load_settings(self):
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                stored = json.load(f)
                self.settings = {**self.defaults, **stored}
        else:
            self.settings = self.defaults
            self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
