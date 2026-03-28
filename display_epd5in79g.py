from typing import Optional
from PIL import ImageChops
from PIL.Image import Image
from waveshare_epd import epd5in79g


class EPD5in79gDisplay:
    """Shows a pre-rendered PIL Image on a Waveshare 5.79inch e-Paper (G) screen."""

    def __init__(self):
        self.epd = epd5in79g.EPD()
        self._prev_image: Optional[Image] = None

    def init(self):
        self.epd.init()
        self.epd.Clear()

    def show(self, image: Image):
        if self._prev_image is not None:
            diff = ImageChops.difference(image, self._prev_image)
            if not diff.getbbox():
                return  # Nothing changed, skip the slow full refresh
        self.epd.display(self.epd.getbuffer(image))
        self._prev_image = image.copy()

    def cleanup(self):
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        epd5in79g.epdconfig.module_exit(cleanup=True)
