from rpi_ws281x import Color, PixelStrip

from metarmap.configuration import config, debug

COLOR_OFF = Color(0, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_GREEN = Color(34, 197, 0)
COLOR_BLUE = Color(31, 112, 219)
COLOR_RED = Color(253, 0, 0)
COLOR_PINK = Color(251, 63, 255)

FLIGHT_CATEGORY_COLORS = {
    'VFR': COLOR_GREEN,
    'MVFR': COLOR_BLUE,
    'IFR': COLOR_RED,
    'LIFR': COLOR_PINK,
}

# Set Up LED Strip
if not debug('LED strip setup'):
    strip = PixelStrip(config['LED'].getint('LED_COUNT'),
                       config['LED'].getint('LED_PIN'),
                       config['LED'].getint('LED_FREQ_HZ'),
                       config['LED'].getint('LED_DMA'),
                       config['LED'].getboolean('LED_INVERT'),
                       config['LED'].getint('LED_BRIGHTNESS'),
                       config['LED'].getint('LED_CHANNEL'))
    strip.begin()


def illuminate_pixel(pixel: int, color: Color = COLOR_WHITE):
    """ Illuminate a single LED pixel """
    if not debug(f'LED {pixel} on, color {color}'):
        strip.setPixelColor(pixel, color)
        strip.show()


def extinguish_pixel(pixel):
    """ Turn a single LED pixel off """
    if not debug(f'LED {pixel} off'):
        strip.setPixelColor(pixel, COLOR_OFF)
        strip.show()
