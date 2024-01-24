import click

from metarmap.configuration import setup_configuration

setup_configuration()


@click.group()
def cli():
    pass


from metarmap.commands.display import clear_display, update_display  # NOQA
from metarmap.commands.lights import clear_lights, pulse_light, update_lights  # NOQA
from metarmap.commands.utils import clear, print_metar, update  # NOQA

cli.add_command(print_metar, name="print")
cli.add_command(pulse_light)
cli.add_command(update_lights)
cli.add_command(clear_lights)
cli.add_command(clear_display)
cli.add_command(update_display)
cli.add_command(update)
cli.add_command(clear)

if __name__ == "__main__":
    cli()
