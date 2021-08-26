from rpi_ws281x import Color, PixelStrip

from metarmap.configuration import config, debug


def get_color(red: str, green: str, blue: str) -> Color:
    """ Return a Color object with red, green, and blue in the apropriate position """
    color_order = [char for char in config['LED'].get('LED_RGB_ORDER', 'RGB')]
    remap = []
    for color in color_order:
        if color.lower() == 'r':
            remap.append(red)
        if color.lower() == 'g':
            remap.append(green)
        if color.lower() == 'b':
            remap.append(blue)
    return Color(*remap)


COLOR_OFF = get_color(0, 0, 0)
COLOR_WHITE = get_color(255, 255, 255)
COLOR_GREEN = get_color(34, 197, 0)
COLOR_BLUE = get_color(31, 112, 219)
COLOR_RED = get_color(253, 0, 0)
COLOR_PINK = get_color(251, 63, 255)
COLOR_YELLOW = get_color(255, 136, 0)

FLIGHT_CATEGORY_COLORS = {
    'VFR': COLOR_GREEN,
    'MVFR': COLOR_BLUE,
    'IFR': COLOR_RED,
    'LIFR': COLOR_PINK,
    'UNK': COLOR_YELLOW,
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
