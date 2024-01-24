import datetime
import os
import textwrap

import click
from PIL import Image, ImageDraw, ImageFont

from metarmap.configuration import config, debug, get_display_lock_content, set_display_lock_content
from metarmap.libraries.aviationweather import metar
from metarmap.libraries.waveshare_epd import epd2in13_V2

FONTDIR = os.path.abspath("/usr/share/fonts/truetype/freefont/")
FONT = ImageFont.truetype(os.path.join(FONTDIR, "FreeSans.ttf"), 13)
FONT_BOLD = ImageFont.truetype(os.path.join(FONTDIR, "FreeSansBold.ttf"), 13)
FONT_TITLE = ImageFont.truetype(os.path.join(FONTDIR, "FreeSans.ttf"), 15)
FONT_TITLE_BOLD = ImageFont.truetype(os.path.join(FONTDIR, "FreeSansBold.ttf"), 15)


@click.command()
def clear_display():
    """Clear the ePaper display"""
    debug("Clear e-paper display")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)


@click.command()
def update_display():
    """Update the ePaper display with current METAR observation"""
    # Fetch Observation
    station = config["SCREEN"].get("airport", None)
    debug(f"Selected airport for e-paper display: {station}")
    if not station:
        return
    try:
        observation = metar.retrieve(
            [
                station,
            ]
        )[0]
        debug(f"Fetched latest weather for station {station}")
    except IndexError:
        debug(f"Weather not found for station {station}")
        return

    # Convert observation time to local (system) timezone
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    timezone_name = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    observation_time_local = observation.get("observation_time").astimezone(timezone)

    # Test observation_time, do not update display if weather observation is not new
    new_lock = f'{station}{observation.get("observation_time")}'
    old_lock = get_display_lock_content()
    if new_lock == old_lock:
        debug(
            f"New weather {new_lock} is the same as old weather {old_lock}. Not updating e-ink display"
        )
        return
    debug(
        f"New weather {new_lock} supersedes old weather {old_lock}. Saving in lockfile."
    )
    set_display_lock_content(new_lock)

    # Initialize Display
    debug("Initialize e-paper display")
    epd = epd2in13_V2.EPD()
    display_width = epd.height
    display_height = epd.width
    epd.init(epd.FULL_UPDATE)
    image = Image.new("1", (display_width, display_height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Title
    debug("Draw title on e-paper display")
    draw.rectangle(((0, 0), (display_width / 2, 22)), fill=0)
    draw.text((2, 0), f"METAR {station}", font=FONT_TITLE_BOLD, fill=255)
    msg = observation_time_local.strftime("%m/%d/%y %H:%M") + timezone_name[0]
    w, h = FONT_TITLE.getsize(msg)
    draw.text(((display_width - w - 2), 0), msg, font=FONT_TITLE)
    draw.line(((0, 22), (display_width, 22)), fill=0, width=1)

    # METAR Text
    debug("Write raw METAR text to e-paper display")
    line_pos = 40
    msg = observation.get("raw_text")
    w, h = FONT.getsize(msg)
    for line in textwrap.wrap(msg, width=34):
        draw.text((0, line_pos), line, font=FONT)
        line_pos += h + 3

    debug("Flush buffered image to e-paper display")
    epd.display(epd.getbuffer(image))
