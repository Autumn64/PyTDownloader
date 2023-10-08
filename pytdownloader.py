import os
import sys
import json
import tkinter as tk
import customtkinter as ctk
from Settings import Settings
from mainFrame import mainFrame
from configFrame import configFrame

class Window(ctk.CTk):
    def __init__(self, settings, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.settings = settings
        self.geometry("600x420")
        self.title("PyTDownloader")
        self.resizable(width=False, height=False)
        self.switchMode = ctk.StringVar(value="dark")
        self.scale = ctk.StringVar(value="1.0")
        self.language = ctk.StringVar(value="en")
        self.currentLang: dict = {}
        self.loadSettings()
        self.mainScreen = mainFrame(self)
        self.configScreen = configFrame(self)
        self.packFrame(self.mainScreen)

    def loadSettings(self) -> None:
        if not os.path.exists(f"{self.settings.route}/settings.json"): self.settings.saveSettings()

        with open(f"{self.settings.route}/settings.json", "r") as f:
            try:
                self.settings.settings = json.load(f)
            except json.JSONDecodeError:
                os.remove(f"{self.settings.route}/settings.json")
                tk.messagebox.showinfo(title="PyTDownloader", message="Something went wrong and we couldn't load your settings.")
                self.settings.saveSettings()

        self.switchMode.set("dark") if self.settings.settings["darkmode"] == True else self.switchMode.set("light")
        self.setMode()

        if self.settings.settings["scaling"] > 3.0: 
            self.scale.set("3.0")
        elif self.settings.settings["scaling"] < 0.5: 
            self.scale.set("0.5")
        else:
            self.scale.set(f"{round(self.settings.settings['scaling'], 2)}")
        self.changeScale()

        try:
            self.language.set(self.settings.settings["language"])
            self.currentLang = languages[self.language.get()]
        except KeyError:
            self.language.set("en")
            self.currentLang = languages["en"]
    
    def setMode(self) -> None:
        if self.switchMode.get() == "dark":
            ctk.set_appearance_mode("dark")
            self.settings.settings["darkmode"] = True
        else:
            ctk.set_appearance_mode("light")
            self.settings.settings["darkmode"] = False
        self.settings.saveSettings()
        self.update()

    def changeScale(self) -> None:
        ctk.set_window_scaling(float(self.scale.get()))
        ctk.set_widget_scaling(float(self.scale.get()))
        self.settings.settings["scaling"] = float(self.scale.get())
        self.settings.saveSettings()
        self.update()

    def setLanguage(self, language: str) -> None:
        self.language.set(self.settings.languages[language])
        self.settings.settings["language"] = self.language.get()
        self.currentLang = languages[self.language.get()]
        self.settings.saveSettings()

    def packFrame(self, frame: ctk.CTkFrame) -> None:
        frame.pack(fill=ctk.BOTH, expand=1)
        self.update()

    def unpackFrame(self, frame: ctk.CTkFrame) -> None:
        frame.pack_forget()
        self.update()

    def switchFrame(self, framedest: ctk.CTkFrame, framesrc: ctk.CTkFrame) -> None:
        self.unpackFrame(framesrc)
        self.packFrame(framedest)

if __name__ == "__main__":
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/languages.json", "r", encoding='utf-8') as f:
        languages: dict = json.load(f)
    settings = Settings()
    root = Window(settings)
    if sys.platform == "win32":
        root.iconbitmap(f'{os.path.dirname(os.path.abspath(__file__))}/icon.ico')
    else:
        root.iconphoto(True, tk.PhotoImage(file=f'{os.path.dirname(os.path.abspath(__file__))}/logo.png'))
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    if len(sys.argv) > 1 and sys.argv[1].startswith("scale="): #This is mostly for GNU/Linux distributions since fractional scaling messes the layout up.
        root.tk.call('tk', 'scaling', float(sys.argv[1].replace("scale=", "").strip()))
        ctk.set_widget_scaling(3)
        root.changeScale()
    root.mainloop()