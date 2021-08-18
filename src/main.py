import click
from commands.utils import print_metar


@click.group()
def cli():
    pass


cli.add_command(print_metar)

if __name__ == '__main__':
    cli()
