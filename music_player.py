import tkinter as tk
from tkinter import filedialog
import pygame
import os
import threading
import datetime
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x310")  # Set the size of the root window
        self.root.configure(bg="#F2F2F2")  # Set background color

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create buttons
        self.btn_load = tk.Button(root, text="Load Music", command=self.load_music, bg="#D5F5E3", fg="#333333", width=10)
        self.btn_play = tk.Button(root, text="Play", command=self.play_music, bg="#82E0AA", fg="#333333", width=10)
        self.btn_pause = tk.Button(root, text="Pause", command=self.pause_music, bg="#FAD7A0", fg="#333333", width=10)
        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_music, bg="#E6B0AA", fg="#333333", width=10)

        # Create slider for volume control
        self.volume_slider = tk.Scale(root, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, label="Volume",
                                      command=self.update_volume, bg="#F2F2F2", troughcolor="#D1D1D1")

        # Create label to display current playing music
        self.lbl_current_music = tk.Label(root, text="Current Music: None", bg="#F2F2F2", fg="#333333")

        # Create song slider
        self.song_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, showvalue=False,
                                    command=self.set_song_position)
        
        # Create label to display song time elapsed
        self.lbl_song_time = tk.Label(root, text="00:00", bg="#F2F2F2", fg="#333333")

        # Set button positions
        self.btn_load.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.btn_play.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.btn_pause.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.btn_stop.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.volume_slider.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.lbl_current_music.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.song_slider.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.lbl_song_time.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Initialize music file path and name
        self.music_file = None
        self.current_music_name = "None"

        # Initialize song position
        self.song_position = 0

        # Create a thread for updating song position
        self.update_position_thread = threading.Thread(target=self.update_song_position)
        self.update_position_thread.daemon = True
        self.update_position_thread.start()

    def load_music(self):
        self.music_file = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if self.music_file:
            self.current_music_name = os.path.basename(self.music_file)
            self.lbl_current_music.config(text="Current Music: " + self.current_music_name)

    def play_music(self):
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_song_position(self):
        while True:
            if pygame.mixer.music.get_busy():
                self.song_position = pygame.mixer.music.get_pos() // 1000
                self.song_slider.set(self.song_position)
                elapsed_time = self.format_time(self.song_position)
                self.lbl_song_time.config(text=elapsed_time)
            else:
                self.song_position = 0
                self.song_slider.set(0)
                self.lbl_song_time.config(text="00:00")
            time.sleep(0.1)  # Add a delay of 0.1 seconds (100ms)
            self.root.update()

    def set_song_position(self, value):
        self.song_position = int(value)
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(self.song_position)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
        return f"{minutes}:{seconds}"

# Create the Tkinter root window
root = tk.Tk()

# Create an instance of the MusicPlayer class
music_player = MusicPlayer(root)

# Run the Tkinter event loop
root.mainloop()
