from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from typing import List, Optional
from api_client import TrainService
from config import display_config


class DepartureBoardRenderer:
    """Renders departure board in LED matrix style."""

    def __init__(self, station_name: str = "", scale: float = 1.0):
        self.width = display_config.WIDTH
        self.height = display_config.HEIGHT
        self.station_name = station_name
        self.scale = scale

        # Create image canvas
        self.image = Image.new('RGB', (self.width, self.height), display_config.BLACK)
        self.draw = ImageDraw.Draw(self.image)

        # Load fonts - try to use a monospace font for authentic LED look
        self.header_font = self._load_font(round(display_config.HEADER_FONT_SIZE * scale))
        self.table_font = self._load_font(round(display_config.TABLE_FONT_SIZE * scale))
        self.row_font = self._load_font(round(display_config.ROW_FONT_SIZE * scale))

    def _load_font(self, size: int) -> ImageFont.ImageFont:
        """Load a font, falling back to default if necessary."""
        try:
            # Try to load a monospace font
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
        except:
            try:
                # Fallback to default monospace
                return ImageFont.truetype("DejaVuSansMono.ttf", size)
            except:
                # Use PIL default font (size= parameter respected in Pillow 10+)
                return ImageFont.load_default(size=size)

    def clear(self):
        """Clear the canvas."""
        self.image = Image.new('RGB', (self.width, self.height), display_config.BLACK)
        self.draw = ImageDraw.Draw(self.image)

    def draw_header(self):
        """Draw the header with station name and current time."""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Draw station name on the left
        if self.station_name:
            self.draw.text(
                (10, 10),
                self.station_name,
                font=self.header_font,
                fill=display_config.WHITE
            )

        # Draw current time on the right
        time_bbox = self.draw.textbbox((0, 0), current_time, font=self.header_font)
        time_width = time_bbox[2] - time_bbox[0]
        self.draw.text(
            (self.width - time_width - 10, 10),
            current_time,
            font=self.header_font,
            fill=display_config.YELLOW
        )

        # Draw a horizontal line below the header
        y_pos = round(display_config.HEADER_HEIGHT * self.scale)
        self.draw.line([(0, y_pos), (self.width, y_pos)], fill=display_config.YELLOW, width=1)

    def draw_table_headers(self):
        """Draw column headers for the departure table."""
        y_pos = round(display_config.HEADER_HEIGHT * self.scale) + 5

        # Column positions
        time_x = 10
        dest_x = 90
        plat_x = 580
        status_x = 650

        # Draw headers
        self.draw.text((time_x, y_pos), "TIME", font=self.table_font, fill=display_config.YELLOW)
        self.draw.text((dest_x, y_pos), "DESTINATION", font=self.table_font, fill=display_config.YELLOW)
        self.draw.text((plat_x, y_pos), "PLAT", font=self.table_font, fill=display_config.YELLOW)
        self.draw.text((status_x, y_pos), "STATUS", font=self.table_font, fill=display_config.YELLOW)

        # Draw a horizontal line below the table headers
        y_pos = round((display_config.HEADER_HEIGHT + display_config.TABLE_HEADER_HEIGHT) * self.scale)
        self.draw.line([(0, y_pos), (self.width, y_pos)], fill=display_config.YELLOW, width=1)

    def draw_service(self, service: TrainService, row_index: int):
        """Draw a single service row."""
        y_pos = round((display_config.HEADER_HEIGHT + display_config.TABLE_HEADER_HEIGHT) * self.scale) + 5 + (row_index * round(display_config.ROW_HEIGHT * self.scale))

        # Column positions
        time_x = 10
        dest_x = 90
        plat_x = 590
        status_x = 650

        # Determine text color based on status
        if service.is_cancelled:
            text_color = display_config.RED
        elif service.is_delayed:
            text_color = display_config.YELLOW
        else:
            text_color = display_config.YELLOW

        # Draw scheduled time
        self.draw.text((time_x, y_pos), service.scheduled_time, font=self.row_font, fill=text_color)

        # Draw destination (truncate if too long)
        max_dest_chars = round(40 / self.scale)
        destination = service.destination
        if len(destination) > max_dest_chars:
            destination = destination[:max_dest_chars - 3] + "..."
        self.draw.text((dest_x, y_pos), destination, font=self.row_font, fill=text_color)

        # Draw platform
        platform = service.platform if service.platform else "-"
        self.draw.text((plat_x, y_pos), platform, font=self.row_font, fill=text_color)

        # Draw status (use red for cancelled/delayed)
        status_color = display_config.RED if (service.is_cancelled or service.is_delayed) else display_config.YELLOW
        status_text = service.status
        if len(status_text) > 15:
            status_text = status_text[:12] + "..."
        self.draw.text((status_x, y_pos), status_text, font=self.row_font, fill=status_color)

    def render(self, services: List[TrainService]) -> Image.Image:
        """
        Render the complete departure board.

        Args:
            services: List of TrainService objects to display

        Returns:
            PIL Image object
        """
        self.clear()
        self.draw_header()
        self.draw_table_headers()

        # Draw each service (limit to what fits on screen)
        scaled_header = round((display_config.HEADER_HEIGHT + display_config.TABLE_HEADER_HEIGHT) * self.scale)
        max_rows = (self.height - scaled_header - 5) // round(display_config.ROW_HEIGHT * self.scale)
        for i, service in enumerate(services[:max_rows]):
            self.draw_service(service, i)

        return self.image

    def save(self, filepath: str):
        """Save the rendered image to a file."""
        self.image.save(filepath)

    def show(self):
        """Display the image (opens in default image viewer)."""
        self.image.show()
