from rpi_ws281x import Color, PixelStrip

from configuration import config

COLOR_WHITE = Color(255, 255, 255)
COLOR_GREEN = Color(34, 197, 0)
COLOR_BLUE = Color(31, 112, 219)
COLOR_RED = Color(253, 0, 0)
COLOR_PINK = Color(251, 63, 255)


# Set Up LED Strip
strip = PixelStrip(config['LED'].getint('LED_COUNT'),
                   config['LED'].getint('LED_PIN'),
                   config['LED'].getint('LED_FREQ_HZ'),
                   config['LED'].getint('LED_DMA'),
                   config['LED'].get('LED_INVERT'),
                   config['LED'].getint('LED_BRIGHTNESS'),
                   config['LED'].getint('LED_CHANNEL'))
strip.begin()


def illuminate_pixel(pixel: int, color: Color = COLOR_WHITE):
    """ Illuminate a single LED pixel """
    strip.setPixelColor(pixel, color)


def extinguish_pixel(pixel):
    """ Turn a single LED pixel off """
    illuminate_pixel(pixel, Color(0, 0, 0))
