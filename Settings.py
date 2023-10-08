import os
import sys
import json

class Settings:
    def __init__(self):
        self.platform: str = sys.platform
        self.route: str
        self.settings: dict = { #Generic settings
            "darkmode": True,
            "scaling": 1.0,
            "language": "en"
        }

        self.languages: dict = {
            "English": "en",
            "Español": "es",
            "Français": "fr",
            "Esperanto": "eo"
        }

        if self.platform == "win32":
            self.route = f"{os.getenv('LOCALAPPDATA')}/pytdownloader"
        else:
            self.route = f"{os.getenv('HOME')}/.pytdownloader"
    
    def saveSettings(self) -> None:
        if not os.path.exists(f"{self.route}/settings.json"):
            try:
                os.mkdir(self.route)
            except FileExistsError: pass
        with open(f"{self.route}/settings.json", "w") as f:
            json.dump(self.settings, f)