import os
import sys
import tkinter as tk
import customtkinter as ctk
from videoDownload import videoDownload
from audioDownload import audioDownload

class mainText():
    def __init__(self, master):
        self.master = master
        self.enterLabel = ctk.StringVar()
        self.downloadBtn = ctk.StringVar()
        self.progressLabel = ctk.StringVar()
        self.cancelBtn = ctk.StringVar()
        self.aboutLabel = ctk.StringVar()
        self.messagebox1 = ctk.StringVar()
        self.messagebox2 = ctk.StringVar()
        self.messagebox3 = ctk.StringVar()
        self.messagebox4 = ctk.StringVar()
        self.messagebox5 = ctk.StringVar()
        self.messagebox6 = ctk.StringVar()
        self.messagebox7 = ctk.StringVar()
        
    def setText(self):
        self.enterLabel.set(value=self.master.currentLang["mainFrame"]["enterLabel"])
        self.downloadBtn.set(value=self.master.currentLang["mainFrame"]["downloadBtn"])
        self.progressLabel.set(value=self.master.currentLang["mainFrame"]["progressLabel"][0])
        self.cancelBtn.set(value=self.master.currentLang["mainFrame"]["cancelBtn"])
        self.aboutLabel.set(value=f'(c) 2023, Autumn64. {self.master.currentLang["mainFrame"]["aboutLabel"]}')
        self.messagebox1.set(value=self.master.currentLang["mainFrame"]["messagebox1"])
        self.messagebox2.set(value=self.master.currentLang["mainFrame"]["messagebox2"])
        self.messagebox3.set(value=self.master.currentLang["mainFrame"]["messagebox3"])
        self.messagebox4.set(value=self.master.currentLang["mainFrame"]["messagebox4"])
        self.messagebox5.set(value=self.master.currentLang["mainFrame"]["messagebox5"])
        self.messagebox6.set(value=self.master.currentLang["mainFrame"]["messagebox6"])
        self.messagebox7.set(value=self.master.currentLang["mainFrame"]["messagebox7"])

class mainFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        ctk.CTkFrame.__init__(self, self.master)
        self.text = mainText(self.master)
        self.configBtn = ctk.CTkButton(self, text="☰", width=20, height=20,
                                       fg_color=("#939ba2", "#3a3a3a"), bg_color=("#939ba2", "#3a3a3a"),
                                       hover_color=("#757b80", "#4a4a4a"), command=lambda currentFrame=self: (
            currentFrame.after(500, master.switchFrame(self.master.configScreen, currentFrame))
        ))
        self.titleLabel = ctk.CTkLabel(self, text="PyTDownloader", font=ctk.CTkFont(size = 30))
        self.enterLabel = ctk.CTkLabel(self, textvariable=self.text.enterLabel, font=ctk.CTkFont(size = 15))
        self.linkInput = ctk.CTkEntry(self, width=450, height=10, placeholder_text="https://youtube.com/...",
                                font=ctk.CTkFont(size = 15), justify=ctk.CENTER,border_width=3)
        self.resCombo = ctk.CTkComboBox(self, values=["1080p", "720p", "480p", "360p", "240p", "144p", "mp3"], state="readonly")
        self.downloadBtn = ctk.CTkButton(self, textvariable=self.text.downloadBtn, font=ctk.CTkFont(size = 15), command=self.download)
        self.progressLabel = ctk.CTkLabel(self, textvariable=self.text.progressLabel)
        self.progressBar = ctk.CTkProgressBar(self, width=500)
        self.cancelBtn = ctk.CTkButton(self, textvariable=self.text.cancelBtn, font=ctk.CTkFont(size = 15), command=self.cancelDownload)
        self.aboutLabel = ctk.CTkLabel(self, textvariable=self.text.aboutLabel, font=ctk.CTkFont(size=10))
        self.text.setText()
        self.packItems()
        
    def packItems(self) -> None:
        self.configBtn.pack(side=ctk.TOP, anchor=ctk.NW, padx=20, pady=10)
        self.titleLabel.pack(pady=10)
        self.enterLabel.pack(pady=10)
        self.linkInput.bind("<Return>", command=lambda args: self.download())
        self.linkInput.pack(pady=20)
        self.resCombo.set("1080p")
        self.resCombo.pack()
        self.downloadBtn.pack(pady=30)
        self.aboutLabel.pack(side=ctk.BOTTOM, pady=15)

    def download(self) -> None:
        if self.resCombo.get() != "mp3":
            video = videoDownload(self)
            video.downloadStart()
        else:
            audio = audioDownload(self)
            audio.downloadStart()
            
        self.clearInput(); self.configBtn.configure(state=ctk.NORMAL); self.resCombo.configure(state="readonly"); self.resCombo.set("1080p")
        self.progressLabel.pack_forget(); self.progressBar.pack_forget(); self.cancelBtn.pack_forget()
        self.downloadBtn.pack(pady=30)
        self.text.setText()
        self.update()

    def cancelDownload(self) -> None:
        tk.messagebox.showinfo(title="PyTDownloader", message=self.text.messagebox4.get())
        os.execl(sys.executable, sys.executable, * sys.argv)

    def updateProgress(self, stream, chunk, bytes_remaining) -> None:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        self.text.progressLabel.set(value=f'{int(bytes_downloaded/total_size*100)}% {self.master.currentLang["mainFrame"]["progressLabel"][2]}')
        self.progressBar.set(float(bytes_downloaded/total_size))
        self.update()

    def clearInput(self) -> None:
        self.linkInput.configure(state=ctk.NORMAL)
        self.linkInput.delete(0, ctk.END)
        self.update()