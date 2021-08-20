import time

import click

from metarmap.configuration import config, debug, get_airport_map
from metarmap.libraries.aviationweather import metar
from metarmap.lighting import FLIGHT_CATEGORY_COLORS, extinguish_pixel, illuminate_pixel


@click.command(no_args_is_help=True)
@click.argument('pixel')
def pulse_light(pixel: int):
    """ Illuminate neopixel at address [PIXEL] for 3 seconds """
    pixel = int(pixel)
    illuminate_pixel(pixel)
    time.sleep(3)
    extinguish_pixel(pixel)


@click.command()
def update_lights():
    """ Update current METAR observation for all airports

    and illuminate all corresponding LED pixels.
    """
    airport_map = get_airport_map()
    airports = [v for v in airport_map.values()]
    observations = metar.retrieve(airports)

    for pixel in airport_map.keys():
        station_name = airport_map[pixel]
        station = [obs for obs in observations if obs.get('station_id') == station_name][0]
        flight_category = station.get('flight_category', 'VFR')
        debug(f'Pixel {pixel} is station {station_name} with current flight category {flight_category}')
        color = FLIGHT_CATEGORY_COLORS.get(flight_category.upper())
        if color:
            illuminate_pixel(pixel, color)
        else:
            extinguish_pixel(pixel)
            debug(f'No color for flight category {flight_category} for station {station_name}')


@click.command()
def clear_lights():
    """ Turn all LED pixels off """
    for pixel in range(config['LED'].getint('LED_COUNT', 0)):
        extinguish_pixel(pixel)
