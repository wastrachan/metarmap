# Metar Map


## Wiring
Connect the LEDs to a GPIO pin, 5V source, and ground pin.


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
The first time you run the `metarmap` command (`metarmap --help`) would be a good place to start,  configuration file is created for you at `~/.config/metarmap/config`.

This INI-style configuration is divided into sections, and will have some defaults pre-filled for you:

```
[MAIN]
debug = off

[LED]
led_count = 50
led_freq_hz = 800000
led_dma = 10
led_brightness = 255
led_invert = false
led_channel = 0
led_pin = 18

[AIRPORTS]
1 = KRYY
```

All of the available configuration option are documented below.

### LED Setup
1. Run `metarmap --help` to verify installation and generate a config file
2. Update the LED section with the appropriate values for your WS2811 LED strip.
3. Run `metarmap pulse-pixel 1` to light up the pixel at address `1`.
4. Continue using the `pulse-pixel` command as necessary to test and map out each LED in your LED strip.


### Airport Setup
Airports are added to the `AIRPORTS` section of the config file, in the format `[PIXEL ID] = [AIRPORT ID]`.

1. Use the `metarmap pulse-pixel` command to determine the ID of the pixel for a given airport.
2. Add the airport to your configuration file with the pixel ID determined in step 1.
3. Repeat this process until all airports have been configured
4. Test your map with `metarmap illuminate`.

An example configuration with four airports:

```
[AIRPORTS]
1 = KRYY
2 = KPDK
4 = KATL
5 = KFTY
```
