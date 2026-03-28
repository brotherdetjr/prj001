import tkinter as tk
from PIL import ImageTk
from PIL.Image import Image
from config import display_config


class TkinterDisplay:
    """Shows a pre-rendered PIL Image in a tkinter window."""

    def __init__(self, station_name: str):
        self.root = tk.Tk()
        self.root.title(f"UK Railway Departures - {station_name}")
        self.root.configure(bg='black')
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=display_config.WIDTH,
            height=display_config.HEIGHT,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()
        self.photo = None

    def show(self, image: Image):
        def _update():
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.after(0, _update)

    def start_mainloop(self):
        self.root.mainloop()
