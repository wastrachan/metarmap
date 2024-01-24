import datetime

import click
from rpi_ws281x import Color, PixelStrip

from metarmap.configuration import config, debug


def get_color(red: str, green: str, blue: str) -> Color:
    """Return a Color object with red, green, and blue in the apropriate position"""
    color_order = [char for char in config["LED"].get("LED_RGB_ORDER", "RGB")]
    remap = []
    for color in color_order:
        if color.lower() == "r":
            remap.append(red)
        if color.lower() == "g":
            remap.append(green)
        if color.lower() == "b":
            remap.append(blue)
    return Color(*remap)


def get_brightness() -> int:
    """Return a brightness intensity based on the configured brightness and the time of day"""
    base_brightness = config["LED"].getint("LED_BRIGHTNESS")
    dimmed_start_time = config["MAIN"].get("DIM_TIME_START")
    dimmed_end_time = config["MAIN"].get("DIM_TIME_END")
    now = datetime.datetime.now()
    try:
        dimmed_brightness = config["MAIN"].getint("DIM_TIME_LED_BRIGHTNESS", 0)
    except ValueError:
        dimmed_brightness = 0
    if dimmed_start_time:
        try:
            dimmed_start_time = datetime.time.fromisoformat(dimmed_start_time)
            dimmed_start_time = now.replace(
                hour=dimmed_start_time.hour,
                minute=dimmed_start_time.minute,
                second=dimmed_start_time.second,
                microsecond=0,
            )
        except (ValueError, TypeError):
            click.echo(
                "dimmed_start_time was provided but not in valid ISO 8601 format"
            )
    if dimmed_end_time:
        try:
            dimmed_end_time = datetime.time.fromisoformat(dimmed_end_time)
            dimmed_end_time = now.replace(
                hour=dimmed_end_time.hour,
                minute=dimmed_end_time.minute,
                second=dimmed_end_time.second,
                microsecond=0,
            )
        except (ValueError, TypeError):
            click.echo("dimmed_end_time was provided but not in valid ISO 8601 format")

    if not all([dimmed_start_time, dimmed_end_time]):
        debug(
            "DIM_TIME_LED_BRIGHTNESS, DIM_TIME_START, and DIM_TIME_END are not all configured. Using LED_BRIGHTNESS"
        )
        return base_brightness

    # Determine if range spans midnight, and compare now with start and end time
    if dimmed_start_time <= dimmed_end_time:
        dim_leds = dimmed_start_time <= now and (dimmed_end_time > now)
    else:
        dim_leds = dimmed_start_time <= now or (dimmed_end_time > now)

    if dim_leds:
        debug(
            f"Current time ({now.isoformat()}) "
            f"is between start ({dimmed_start_time.isoformat()}) "
            f"and end ({dimmed_end_time.isoformat()}). Using dimmed brightness."
        )
        return dimmed_brightness
    else:
        debug(
            f"Current time ({now.isoformat()}) "
            f"is not between start ({dimmed_start_time.isoformat()}) "
            f"and end ({dimmed_end_time.isoformat()}). Using default brightness."
        )
        return base_brightness


COLOR_OFF = get_color(0, 0, 0)
COLOR_WHITE = get_color(255, 255, 255)
COLOR_GREEN = get_color(34, 197, 0)
COLOR_BLUE = get_color(31, 112, 219)
COLOR_RED = get_color(253, 0, 0)
COLOR_PINK = get_color(251, 63, 255)
COLOR_YELLOW = get_color(255, 136, 0)

FLIGHT_CATEGORY_COLORS = {
    "VFR": COLOR_GREEN,
    "MVFR": COLOR_BLUE,
    "IFR": COLOR_RED,
    "LIFR": COLOR_PINK,
    "UNK": COLOR_YELLOW,
}


# Set Up LED Strip
brightness = get_brightness()
if not debug("LED strip setup"):
    strip = PixelStrip(
        config["LED"].getint("LED_COUNT"),
        config["LED"].getint("LED_PIN"),
        config["LED"].getint("LED_FREQ_HZ"),
        config["LED"].getint("LED_DMA"),
        config["LED"].getboolean("LED_INVERT"),
        brightness,
        config["LED"].getint("LED_CHANNEL"),
    )
    strip.begin()


def illuminate_pixel(pixel: int, color: Color = COLOR_WHITE):
    """Illuminate a single LED pixel"""
    if not debug(f"LED {pixel} on, color {color}"):
        strip.setPixelColor(pixel, color)
        strip.show()


def extinguish_pixel(pixel):
    """Turn a single LED pixel off"""
    if not debug(f"LED {pixel} off"):
        strip.setPixelColor(pixel, COLOR_OFF)
        strip.show()
