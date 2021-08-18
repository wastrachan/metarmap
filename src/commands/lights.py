import time

import click

from lighting import extinguish_pixel, illuminate_pixel


@click.command(no_args_is_help=True)
@click.argument('pixel')
def pulse_pixel(pixel: int):
    """ Illuminate neopixel at address [PIXEL] for 5 seconds """
    pixel = int(pixel)
    click.echo(f'Illuminating pixel {pixel}')
    illuminate_pixel(pixel)
    time.sleep(5)
    extinguish_pixel(pixel)
