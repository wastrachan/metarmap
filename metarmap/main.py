import click

from metarmap.configuration import setup_configuration

setup_configuration()


@click.group()
def cli():
    pass


from metarmap.commands.lights import clear, pulse, update  # NOQA
from metarmap.commands.utils import print_metar  # NOQA

cli.add_command(print_metar, name='print')
cli.add_command(pulse)
cli.add_command(update)
cli.add_command(clear)

if __name__ == '__main__':
    cli()
