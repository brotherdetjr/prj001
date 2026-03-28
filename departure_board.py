#!/usr/bin/env python3
"""
UK Railway Departure Board
Displays real-time departure information in LED matrix style.
"""

import sys
import time
import threading
from datetime import datetime
from api_client import client
from renderer import DepartureBoardRenderer
from config import api_config


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
    return STATION_NAMES.get(station_code.upper(), station_code.upper())


def run_loop(display, station_code: str, station_name: str):
    """Fetch departures, render to PIL Image, and push to display — indefinitely."""
    renderer = DepartureBoardRenderer(station_name=station_name)
    print(f"Starting departure board for {station_name} ({station_code})")
    print(f"Refresh interval: {api_config.REFRESH_INTERVAL} seconds")
    while True:
        try:
            services = client.get_departures(station_code, api_config.NUM_SERVICES)
            if services:
                image = renderer.render(services)
                display.show(image)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Updated")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No services found")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        time.sleep(api_config.REFRESH_INTERVAL)


def main():
    station_code = api_config.STATION_CODE
    station_name = get_station_name(station_code)

    if '--epd5in79g' in sys.argv:
        from display_epd5in79g import EPD5in79gDisplay
        display = EPD5in79gDisplay()
        display.init()
        try:
            run_loop(display, station_code, station_name)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            display.cleanup()
    else:
        from display_tkinter import TkinterDisplay
        display = TkinterDisplay(station_name)
        thread = threading.Thread(
            target=run_loop,
            args=(display, station_code, station_name),
            daemon=True
        )
        thread.start()
        try:
            display.start_mainloop()
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    main()
