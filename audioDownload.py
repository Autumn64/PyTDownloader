import os
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from pytube import YouTube, Stream

class audioDownload():
    def __init__(self, frame: ctk.CTkFrame):
        self.frame = frame;

    def downloadStart(self) -> None:
        link: str = self.frame.linkInput.get()
        if link.strip() == "": return
        self.frame.downloadBtn.pack_forget()
        self.frame.progressLabel.pack(pady=10)
        self.frame.update()
        try:
            youtube = YouTube(link, on_progress_callback=self.frame.updateProgress)
            audio: Stream = youtube.streams.filter(only_audio=True)[0]
            if audio == None:
                tk.messagebox.showerror(title="PyTDownloader", message=self.frame.text.messagebox7.get())
                return
            self.downloadAudio(audio);
        except Exception as e:
            if str(e).startswith("regex_search:"):
                tk.messagebox.showerror(title="PyTDownloader", message=f'{link} {self.frame.text.messagebox3.get()}')
            elif str(e) == "cancel":
                tk.messagebox.showinfo(title="PyTDownloader", message=self.frame.text.messagebox4.get())
            else:
                tk.messagebox.showerror(title="PyTDownloader", message=f'{self.frame.text.messagebox5.get()} {e}')
        else:
            tk.messagebox.showinfo(title="PyTDownloader", message=self.frame.text.messagebox6.get())
    
    def downloadAudio(self, audio: Stream) -> None:
        path: str = filedialog.askdirectory()
        if (len(path) == 0): raise Exception("cancel")
        self.frame.progressBar.set(0); self.frame.progressBar.pack(); self.frame.cancelBtn.pack(pady=15)
        self.frame.text.progressLabel.set(value=self.frame.master.currentLang["mainFrame"]["progressLabel"][1])
        self.frame.configBtn.configure(state=ctk.DISABLED); self.frame.linkInput.configure(state=ctk.DISABLED); self.frame.resCombo.configure(state=ctk.DISABLED)
        self.frame.update()
        audio_name: str = audio.default_filename
        audio.download(output_path=path, filename=f"audio-{audio_name}")
        self.convertAudio(path, audio.title, f"{path}/audio-{audio_name}")
    
    def convertAudio(self, path: str, title: str, audio_name: str) -> None:
        correct_title: str = ""
        for char in title:
            if char not in ('*', '?', '"', '<', '>', '|', ':', '/', '\\'):
                correct_title += char
        self.frame.text.progressLabel.set(value=self.frame.master.currentLang["mainFrame"]["progressLabel"][4])
        self.frame.cancelBtn.pack_forget()
        self.frame.update()
        ffmpeg_exec: str = f"{os.path.dirname(os.path.abspath(__file__))}/ffmpeg.exe" if self.frame.master.settings.platform == "win32" else f'{os.path.dirname(__file__)}/ffmpeg'
        result: subprocess.CompletedProcess = subprocess.run(f'"{ffmpeg_exec}" -hide_banner -loglevel level+warning -y -i "{audio_name}" "{path}/{correct_title}.mp3"', shell=True, stderr=subprocess.PIPE, text=True)
        if result.stderr != "": raise Exception(result.stderr)
        os.remove(audio_name)
