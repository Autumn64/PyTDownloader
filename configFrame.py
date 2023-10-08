import os
import sys
import tkinter as tk
import customtkinter as ctk

class configText():
    def __init__(self, master):
        self.master = master
        self.titleLabel = ctk.StringVar()
        self.modeLabel = ctk.StringVar()
        self.langLabel = ctk.StringVar()
        self.scaleLabel = ctk.StringVar()
        self.resetBtn = ctk.StringVar()
        self.messagebox1 = ctk.StringVar()
        self.messagebox2 = ctk.StringVar()
    
    def setText(self):
        self.titleLabel.set(value=self.master.currentLang["configFrame"]["titleLabel"])
        self.modeLabel.set(value=self.master.currentLang["configFrame"]["modeLabel"])
        self.langLabel.set(value=self.master.currentLang["configFrame"]["langLabel"])
        self.scaleLabel.set(value=self.master.currentLang["configFrame"]["scaleLabel"])
        self.resetBtn.set(value=self.master.currentLang["configFrame"]["resetBtn"])
        self.messagebox1.set(value=self.master.currentLang["configFrame"]["messagebox1"])
        self.messagebox2.set(value=self.master.currentLang["configFrame"]["messagebox2"])

class configFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        ctk.CTkFrame.__init__(self, self.master)
        self.text = configText(self.master)
        self.modeFrame = ctk.CTkFrame(self, border_width=0, width=200, fg_color="transparent") #Frame for dark mode switch
        self.scaleFrame = ctk.CTkFrame(self, border_width=0) #Frame for scaling items
        self.goBackBtn = ctk.CTkButton(self, text="←", width=20, height=20,
                                       fg_color=("#939ba2", "#3a3a3a"), bg_color=("#939ba2", "#3a3a3a"),
                                       hover_color=("#757b80", "#4a4a4a"), command=lambda currentFrame=self: (
            currentFrame.after(500, self.master.switchFrame(self.master.mainScreen, currentFrame))
        ))
        self.titleLabel = ctk.CTkLabel(self, textvariable=self.text.titleLabel, font=ctk.CTkFont(size = 30))
        self.modeLabel = ctk.CTkLabel(self.modeFrame, textvariable=self.text.modeLabel, font=ctk.CTkFont(size = 20))
        self.emptyModeLabel = ctk.CTkLabel(self.modeFrame, text="dadas")
        self.modeSwitch = ctk.CTkSwitch(self.modeFrame, command=master.setMode, text=None,
                                        variable=master.switchMode, onvalue="dark", offvalue="light")
        self.langLabel = ctk.CTkLabel(self, textvariable=self.text.langLabel, font=ctk.CTkFont(size=20))
        self.langCombo = ctk.CTkComboBox(self, values=["English", "Español", "Français", "Esperanto"], state="readonly", command=self.changeLanguage)
        self.scaleLabel = ctk.CTkLabel(self, textvariable=self.text.scaleLabel, font=ctk.CTkFont(size = 20))
        self.scaleInput = ctk.CTkEntry(self.scaleFrame, width=55, height=30, textvariable=master.scale, corner_radius=0, font=ctk.CTkFont(size = 15), justify=ctk.CENTER, border_width=1)
        self.scalepBtn = ctk.CTkButton(self.scaleFrame, width=30, height=30, text="+", corner_radius=0, font=ctk.CTkFont(size = 15), command=lambda: self.stepScale(0.1))
        self.scalemBtn = ctk.CTkButton(self.scaleFrame, width=30, height=30, text="-", corner_radius=0, font=ctk.CTkFont(size = 15), command=lambda: self.stepScale(-0.1))
        self.resetBtn = ctk.CTkButton(self, textvariable=self.text.resetBtn, font=ctk.CTkFont(size = 15), command=self.resetSettings)

        self.text.setText()
        self.packItems()

    def packItems(self) -> None:
        self.goBackBtn.pack(side=ctk.TOP, anchor=ctk.NW, padx=20, pady=10)
        self.titleLabel.pack(pady=10)
        self.modeFrame.grid_columnconfigure(1, weight=1)
        self.modeLabel.grid(row=0, column=0, padx=60)
        self.modeSwitch.grid(row=0, column=1)
        self.modeFrame.pack(pady=10)
        self.langLabel.pack(pady=10)
        self.langCombo.set([key for key, value in self.master.settings.languages.items() if value == self.master.language.get()][0])
        self.langCombo.pack()
        self.scaleLabel.pack(pady=10)
        self.scaleInput.grid(row=0, column=0)
        self.scaleInput.bind("<Return>", command=lambda args: self.updateScale())
        self.scalemBtn.grid(row=0, column=1)
        self.scalepBtn.grid(row=0, column=2)
        self.scaleFrame.pack()
        self.resetBtn.pack(pady=25)

    def stepScale(self, step: float) -> None:
        dot_count: int = 0
        correct_scale: str = ""
        for char in self.scaleInput.get():
            if char not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."): continue
            if char == "." and dot_count == 0: dot_count += 1
            elif char == "." and dot_count > 0: continue
            correct_scale += char

        currentScale: float = round(float(correct_scale), 2)
        if currentScale + step < 0.5 or currentScale + step > 3.0: return
        self.master.scale.set(f"{round(currentScale + step, 2)}")
        self.master.changeScale()

    def updateScale(self) -> None:
        dot_count: int = 0
        correct_scale: str = ""
        for char in self.scaleInput.get():
            if char not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."): continue
            if char == "." and dot_count == 0: dot_count += 1
            elif char == "." and dot_count > 0: continue
            correct_scale += char

        correct_scale: float = round(float(correct_scale), 2)
        if correct_scale < 0.5:
            correct_scale = 0.5
        elif correct_scale > 3.0:
            correct_scale = 3.0
        self.master.scale.set(f"{round(correct_scale, 2)}")
        self.master.changeScale()

    def changeLanguage(self, language: str) -> None:
        self.master.setLanguage(language)
        self.text.setText()
        self.master.mainScreen.text.setText()
        self.update()
    
    def resetSettings(self) -> None:
        reset = tk.messagebox.askyesno(title="PyTDownloader", message=self.text.messagebox1.get())
        if not reset: return
        os.remove(f"{self.master.settings.route}/settings.json")
        tk.messagebox.showinfo(title="PyTDownloader", message=self.text.messagebox2.get())
        os.execl(sys.executable, sys.executable, * sys.argv)