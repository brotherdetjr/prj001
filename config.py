import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class DisplayConfig:
    """Display configuration constants."""
    WIDTH: int = 792
    HEIGHT: int = 272

    # Color palette
    BLACK: tuple = (0, 0, 0)
    WHITE: tuple = (255, 255, 255)
    YELLOW: tuple = (255, 255, 0)  # #FFD700
    RED: tuple = (255, 0, 0)  # #FF0000

    # Layout dimensions
    HEADER_HEIGHT: int = 40
    TABLE_HEADER_HEIGHT: int = 30
    ROW_HEIGHT: int = 30

    # Font sizes
    HEADER_FONT_SIZE: int = 23
    TABLE_FONT_SIZE: int = 18
    ROW_FONT_SIZE: int = 19


@dataclass
class APIConfig:
    """API configuration."""
    BASE_URL: str = "https://national-rail-api.davwheat.dev"
    STATION_CODE: str = os.getenv("STATION_CODE", "PAD")  # Default: London Paddington
    API_TOKEN: str = os.getenv("API_TOKEN", "")
    NUM_SERVICES: int = int(os.getenv("NUM_SERVICES", "8"))
    REFRESH_INTERVAL: int = int(os.getenv("REFRESH_INTERVAL", "60"))  # seconds


# Global config instances
display_config = DisplayConfig()
api_config = APIConfig()
