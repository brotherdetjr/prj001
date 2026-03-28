#!/usr/bin/env python3
"""
UK Railway Departure Board
Displays real-time departure information in LED matrix style.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import sys
from datetime import datetime
from api_client import client
from renderer import DepartureBoardRenderer
from config import api_config


# Station name mapping (you can expand this)
STATION_NAMES = {
    "PAD": "London Paddington",
    "KGX": "London King's Cross",
    "EUS": "London Euston",
    "VIC": "London Victoria",
    "WAT": "London Waterloo",
    "LBG": "London Bridge",
    "LST": "London Liverpool Street",
    "STP": "London St Pancras",
    "CHX": "London Charing Cross",
    "MAN": "Manchester Piccadilly",
    "BHM": "Birmingham New Street",
    "GLC": "Glasgow Central",
    "EDB": "Edinburgh Waverley",
    "MZH": "Maze Hill"
}


def get_station_name(station_code: str) -> str:
    """Get the full station name from the code."""
    return STATION_NAMES.get(station_code.upper(), station_code.upper())


class DepartureBoardGUI:
    """GUI window for displaying the departure board."""

    def __init__(self, root, station_code, station_name):
        self.root = root
        self.station_code = station_code
        self.station_name = station_name
        self.renderer = DepartureBoardRenderer(station_name=station_name)

        # Setup window
        self.root.title(f"UK Railway Departures - {station_name}")
        self.root.configure(bg='black')
        self.root.resizable(False, False)

        # Create canvas for image display
        self.canvas = tk.Canvas(
            root,
            width=792,
            height=272,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()

        # Keep reference to photo image
        self.photo = None

        # Initial update
        print(f"Starting departure board for {station_name} ({station_code})")
        print(f"Refresh interval: {api_config.REFRESH_INTERVAL} seconds")
        self.update_board()

    def update_board(self):
        """Fetch and display updated departure information."""
        try:
            # Fetch departures
            services = client.get_departures(self.station_code, api_config.NUM_SERVICES)

            if services:
                # Render the board
                image = self.renderer.render(services)

                # Convert to PhotoImage for tkinter
                self.photo = ImageTk.PhotoImage(image)

                # Update canvas
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

                # Console output
                now = datetime.now().strftime('%H:%M:%S')
                print(f"[{now}] Updated")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No services found")

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")

        # Schedule next update
        self.root.after(api_config.REFRESH_INTERVAL * 1000, self.update_board)

    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


def main():
    """Main application entry point."""
    station_code = api_config.STATION_CODE
    station_name = get_station_name(station_code)

    # Create GUI window
    root = tk.Tk()

    try:
        app = DepartureBoardGUI(root, station_code, station_name)
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        messagebox.showerror("Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
