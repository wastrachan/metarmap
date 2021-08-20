import os
import textwrap

import click
from PIL import Image, ImageDraw, ImageFont

from metarmap.configuration import config
from metarmap.libraries.aviationweather import metar
from metarmap.libraries.waveshare_epd import epd2in13_V2

FONTDIR = os.path.abspath('/usr/share/fonts/truetype/freefont/')
FONT = ImageFont.truetype(os.path.join(FONTDIR, 'FreeSans.ttf'), 13)
FONT_BOLD = ImageFont.truetype(os.path.join(FONTDIR, 'FreeSansBold.ttf'), 13)
FONT_TITLE = ImageFont.truetype(os.path.join(FONTDIR, 'FreeSans.ttf'), 15)
FONT_TITLE_BOLD = ImageFont.truetype(os.path.join(FONTDIR, 'FreeSansBold.ttf'), 15)


@click.command()
def clear_display():
    """ Clear the ePaper display """
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)


@click.command()
def update_display():
    """ Update the ePaper display with current METAR observation """
    # Fetch Observation
    station = config['SCREEN'].get('airport', None)
    if not station:
        return
    try:
        observation = metar.retrieve([station, ])[0]
    except IndexError:
        return

    # Initialize Display
    epd = epd2in13_V2.EPD()
    display_width = epd.height
    display_height = epd.width
    margin = 10
    epd.init(epd.FULL_UPDATE)
    image = Image.new('1', (display_width, display_height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Title
    draw.rectangle(((0, 0), (display_width / 2, 22)), fill=0)
    draw.text((2, 0), f'METAR {station}', font=FONT_TITLE_BOLD, fill=255)
    msg = observation.get('observation_time').strftime('%m/%d/%y %H:%MZ')
    w, h = FONT_TITLE.getsize(msg)
    draw.text(((display_width - w - 2), 0), msg, font=FONT_TITLE)
    draw.line(((0, 22), (display_width, 22)), fill=0, width=1)

    # METAR Text
    line_pos = 40
    msg = observation.get('raw_text')
    w, h = FONT.getsize(msg)
    for line in textwrap.wrap(msg, width=80):
        draw.text((0, line_pos), line, font=FONT)
        line_pos += h + margin

    epd.display(epd.getbuffer(image))
