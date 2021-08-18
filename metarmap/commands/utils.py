import click

from metarmap.libraries.aviationweather import metar


@click.command(no_args_is_help=True)
@click.argument('station')
def print_metar(station: str):
    """ Display the most recent METAR for [STATION]

    STATION should be a four-letter station identifier (e.g. KRYY)
    """
    station = station.upper()
    if metar_result := metar.retrieve([station, ]):
        metar_text = metar_result[0].get('raw_text')
        click.echo(f'Latest Surface Observation for {station}:\n\n{metar_text}')
    else:
        click.echo(f'No observation for {station}')
