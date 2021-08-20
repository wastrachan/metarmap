import click

from metarmap.commands.display import clear_display, update_display
from metarmap.commands.lights import clear_lights, update_lights
from metarmap.libraries.aviationweather import metar


@click.command(no_args_is_help=True)
@click.argument('station')
def print_metar(station: str):
    """ Display the most recent METAR for [STATION]

    STATION should be a four-letter station identifier (e.g. KRYY)
    """
    station = station.upper()
    metar_result = metar.retrieve([station, ])
    if metar_result:
        metar_text = metar_result[0].get('raw_text')
        click.echo(f'Latest Surface Observation for {station}:\n\n{metar_text}')
    else:
        click.echo(f'No observation for {station}')


@click.command()
@click.pass_context
def update(ctx):
    """ Update lights and e-Paper display """
    ctx.invoke(update_lights)
    ctx.invoke(update_display)


@click.command()
@click.pass_context
def clear(ctx):
    """ Turn of all LED pixels off and lcear e-Paper display """
    ctx.invoke(clear_lights)
    ctx.invoke(clear_display)
