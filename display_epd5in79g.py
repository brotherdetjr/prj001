from PIL.Image import Image
from waveshare_epd import epd5in79g


class EPD5in79gDisplay:
    """Shows a pre-rendered PIL Image on a Waveshare 5.79inch e-Paper (G) screen."""

    def __init__(self):
        self.epd = epd5in79g.EPD()

    def init(self):
        self.epd.init()
        self.epd.Clear()

    def show(self, image: Image):
        self.epd.display(self.epd.getbuffer(image))

    def cleanup(self):
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        epd5in79g.epdconfig.module_exit(cleanup=True)
