# METAR Map


## Wiring
Connect the LEDs to a GPIO pin, 5V source, and ground pin. Do the math on your current requirements, and do not power the LEDs from your Pi if the amperage exceeds safe limits.

## Installation
Your Raspberry Pi should be set up and connected to WiFi at this point. This README will not cover the fundamentals of using a Pi.

```
$ sudo apt install python3-pip libxslt-dev
$ git clone https://github.com/wastrachan/metarmap.git
$ cd metarmap
$ sudo pip3 install .
```
**Why Sudo**? Accessing the GPIO pins with the `rpi-ws281x` library requires access to `/dev/mem` - which can't be accessed by a non-root user. That means that running (and installing `metarmap`) must be done with sudo.


## Configuration
The first time you run the `metarmap` command (`metarmap --help` would be a good place to start), configuration file is created for you at `/root/.config/metarmap/config`.

This INI-style configuration is divided into sections, and will have some defaults pre-filled for you:

```
[MAIN]
debug = off

[LED]
led_count = 10
led_freq_hz = 800000
led_dma = 10
led_brightness = 255
led_invert = false
led_channel = 0
led_pin = 18
led_rgb_order = rgb

[AIRPORTS]
0 = KATL
```

All of the available configuration option are documented below.

### LED Setup
1. Run `metarmap --help` to verify installation and generate a config file
2. Update the LED section with the appropriate values for your WS2811 LED strip.
3. Run `metarmap pulse 0` to light up the pixel at address `0`.
4. Continue using the `pulse` command as necessary to test and map out each LED in your LED strip.


### Airport Setup
Airports are added to the `AIRPORTS` section of the config file, in the format `[PIXEL ID] = [AIRPORT ID]`.

1. Use the `metarmap pulse` command to determine the ID of the pixel for a given airport.
2. Add the airport to your configuration file with the pixel ID determined in step 1.
3. Repeat this process until all airports have been configured
4. Test your map with `metarmap illuminate`.

An example configuration with four airports:

```
[AIRPORTS]
0 = KRYY
2 = KPDK
4 = KATL
5 = KFTY
```

### Configuration Options
Many of the configuration options can be left alone. Expect to change `led_count` and `led_pin`, as well as `AIRPORTS`.

| Section | Option           | Default  | Description
|---------|------------------|----------|------------
| `MAIN`  | `debug`          | `off`    | Enable debug mode. When debug mode is on, additional output is generated and LED actions are simulated only.
| `LED`   | `led_count`      | `10`     | Total number of LED's in your WS2811 LED strip
| `LED`   | `led_freq_hz`    | `800000` | Pulse wavelength frequency for WS2811 LED's. The default (800KHz) should be appropriate in most cases.
| `LED`   | `led_dma`        | `10`     | DMA channel for signal generation. The default should be appropriate in most cases.
| `LED`   | `led_brightness` | `255`    | LED brightness, on a scale of 0 (off) to 255 (maximum).
| `LED`   | `led_invert`     | `false`  | Invert the LED signal (when using NPN transistor level shift)
| `LED`   | `led_channel`    | `0`      | LED output channel (0-2).
| `LED`   | `led_pin`        | `18`     | Raspberry Pi GPIO Pin for LED control.
| `LED`   | `led_rgb_order`  | `rgb`    | Typically color is specific as RGB, but some strips expect GRB. Change this if RGB channels appear swapped.

## Usage

```
Usage: metarmap [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  extinguish   Turn all LED pixels off
  illuminate   Update current METAR observation for all airports
  print-metar  Display the most recent METAR for [STATION]
  pulse  Illuminate neopixel at address [PIXEL] for 3 seconds
```
