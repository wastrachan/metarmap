import click

from metarmap.configuration import setup_configuration

setup_configuration()


@click.group()
def cli():
    pass


from metarmap.commands.lights import extinguish, illuminate, pulse_pixel  # NOQA
from metarmap.commands.utils import print_metar  # NOQA

cli.add_command(print_metar)
cli.add_command(pulse_pixel)
cli.add_command(illuminate)
cli.add_command(extinguish)

if __name__ == '__main__':
    cli()
