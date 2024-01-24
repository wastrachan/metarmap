# METAR Map

There are several "METAR Map" projects out there, and there will probably be more popping up each year. As an avid aviator, it was only a matter of time before I needed one hanging above my own desk.

This project takes inspiration from everybody before me who has shared their work and builds-- but as a developer, I was never going to be happy unless I went through the exercise of writing the software myself. This project has only ever been tested in my own build and carries no warranty, express or implied. I share it in the hope that it too will inspire the next generation of METAR maps.

## Bill of Materials

For this specific build, I used:

-   Raspberry Pi Zero W
-   [WS2811 Individually Addressable LED Pixels](https://www.amazon.com/gp/product/B01AG923GI)
-   [Printed Foam Poster (FedEx Office)](https://www.fedex.com/en-us/printing/posters/mounted.html)
    -   Sectional images were downloaded [from the FAA](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/) and cropped before uploading to FedEx.
-   [2.13" e-Paper Display](https://www.amazon.com/gp/product/B07Z1WYRQH/)

## Wiring

The physical setup/wiring progress is not covered in depth by this README. It is possible I'll take photos and document the process if I build another map in the future.

Connect the LEDs to a GPIO pin, 5V source, and ground pin. Do the math on your LEDs' current requirements, and **do not power the LEDs from your Pi if the amperage exceeds safe limits**.

On the Pi Zero W in my project:

### LEDs

| Pin | Function |
| --- | -------- |
| 2   | + 5 VDC  |
| 6   | Ground   |
| 18  | DIN      |

### ePaper Display

| Pin | Function |
| --- | -------- |
| 1   | VCC      |
| 9   | GND      |
| 19  | DIN      |
| 23  | CLK      |
| 24  | CS       |
| 22  | DC       |
| 11  | RST      |
| 18  | BUSY     |

## Installation

### Install Raspberry Pi OS

Abbreviated headless installation instructions have been included for reference. Words in all caps surrounded by brackets (`<ALL_CAPS>`) should be replaced. You can do this on your own or with the Raspberry Pi imager, if you wish. Just make sure that however you install that **SPI is enabled**, as it is required by this project.

```shell
# 1. Download Raspberry Pi OS Lite (https://www.raspberrypi.com/software/operating-systems/)
$ curl -O https://downloads.raspberrypi.com/raspios_lite_armhf/images/raspios_lite_armhf-2023-12-11/2023-12-11-raspios-bookworm-armhf-lite.img.xz

# 2. Extract the downloaded image, copy to SD card (assuming SD card is /dev/sda)
$ xz -d 2023-12-11-raspios-bookworm-armhf-lite.img.xz
$ sudo dd if=2023-12-11-raspios-bookworm-armhf-lite.img of=/dev/sda bs=8M oflag=sync status=progress

# 3. Mount the boot partition of the SD card (Referenced as <MOUNT_LOCATION> below)

# 4. Create a new user, enable SSH
$ cd <MOUNT_LOCATION>/bootfs
$ echo "<MY_USERNAME>:$(echo '<MY_PASSWORD>' | openssl passwd -6 -stdin)" > userconf.txt
$ touch ssh

# 5. Enable SPI
sed -i '/dtparam=spi/s/^#//g' config.txt

# 4. Configure Wifi
$ cd <MOUNT LOCATION>/rootfs
$ sudo tee etc/NetworkManager/system-connections/WiFi.nmconnection <<EOF
[connection]
id=WiFi
type=wifi
interface-name=wlan0

[wifi]
mode=infrastructure
ssid=<WIFI_SSID>

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=<WIFI_PASSWORD>

[ipv4]
method=auto

[ipv6]
addr-gen-mode=default
method=auto

[proxy]
EOF
$ sudo chown root:root etc/NetworkManager/system-connections/WiFi.nmconnection
$ sudo chmod 0600 etc/NetworkManager/system-connections/WiFi.nmconnection

# 5. Unmount the SD card. Install it in the Pi, and boot
```

### Install BCM2835 Libraries

```shell
$ curl -O http://www.airspayce.com/mikem/bcm2835/bcm2835-1.73.tar.gz
$ tar -axf bcm2835-1.1.73.tar.gz
$ cd bcm2835-1.1.73/
$ sudo ./configure
$ sudo make
$ sudo make check
$ sudo make install
```

### Install Dependencies:

```shell
$ sudo apt install \
    git \
    python3-dev \
    pipx \
    libopenjp2-7 \
    libopenjp2-7-dev \
    libxslt1-dev \
    fonts-freefont-ttf
```

### Install Package:

```shell
$ git clone https://github.com/wastrachan/metarmap.git
$ cd metarmap
$ sudo -i pipx install .
$ sudo -i pipx ensurepath
```

**Why Sudo?** Accessing the GPIO pins with the `rpi-ws281x` library requires access to `/dev/mem`, which can't be accessed by a non-root user. That means that running (and installing `metarmap`) must be done with sudo.

### Run Automatically

A systemd unit file and timer have been provided to automate the update process. They should be manually copied into place if you wish to use them. If not, you'll need to rely on CRON or your own unit files to handle automation.

```shell
$ cd metarmap
$ sudo cp systemd/metarmap.service /etc/systemd/system/
$ sudo cp systemd/metarmap.timer /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable metarmap.service
$ sudo systemctl enable metarmap.timer
$ sudo systemctl start metarmap.timer
$ sudo systemctl list-timers
NEXT                         LEFT          LAST                         PASSED       UNIT                         ACTIVATES
Fri 2021-08-20 19:00:00 BST  1min 22s left n/a                          n/a          metarmap.timer               metarmap.service

```

## Configuration

The first time you run `metarmap` (`sudo -i metarmap --help` would be a good place to start), a configuration file is created for you at `/root/.config/metarmap/config`.

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

[SCREEN]
airport = KATL
```

All of the available configuration option are documented below.

### LED Setup

1. Run `metarmap --help` to verify installation and generate a config file
2. Update the LED section with the appropriate values for your WS2811 LED strip. Expect to change `led_count` and `led_pin`. The rest of the settings can typically be left alone.
3. Run `metarmap pulse 0` to light up the pixel at address `0`.
4. Continue using the `pulse` command as necessary to test and map out each LED in your LED strip.

### Airport Setup

Airports are added to the `AIRPORTS` section of the config file, in the format `[PIXEL ID] = [AIRPORT ID]`.

1. Use the `metarmap pulse` command to determine the ID of the pixel for a given airport.
2. Add the airport to your configuration file with the pixel ID determined in step 1.
3. Repeat this process until all airports have been configured
4. Test your map with `metarmap update`.

An example configuration with four airports:

```
[AIRPORTS]
0 = KATL
1 = KRYY
2 = KPDK
3 = KFTY
```

### E-Ink Display

The e-ink display will present the METAR observation at one static airport. This is configured via the `airport` setting in the `SCREEN` section:

```
[SCREEN]
airport = KATL
```

### Configuration Options

Many of the configuration options can be left alone. Expect to change `led_count` and `led_pin`, as well as `AIRPORTS`.

| Section  | Option                    | Default  | Description                                                                                                                                                                                                                                                                                                                               |
| -------- | ------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MAIN`   | `debug`                   | `off`    | Enable debug mode. When debug mode is on, additional output is generated and LED actions are simulated only.                                                                                                                                                                                                                              |
| `MAIN`   | `dim_time_start`          |          | If provided, the LED brightness will be set to `dim_time_led_brightness` during the hours between this value and `dim_time_end`. `dim_time_start`, `dim_time_end`, and `dim_time_led_brightness` all must be set for this feature to take effect. The time provided should be expressed in hours local time (e.x. `23:00`).               |
| `MAIN`   | `dim_time_end`            |          | If provided, the LED brightness will be set to `dim_time_led_brightness` during the hours between `dim_time_start` and this value. `dim_time_start`, `dim_time_end`, and `dim_time_led_brightness` all must be set for this feature to take effect. The time provided should be expressed in hours local time (e.x. `07:00`).             |
| `MAIN`   | `dim_time_led_brightness` | `20`     | If `dim_time_start` and `dim_time_end` are set, the LED brightness will be set to this value between `dim_time_start` and `dim_time_end`. `dim_time_start`, `dim_time_end`, and `dim_time_led_brightness` all must be set for this feature to take effect. If this is set to `0`, the lights will be disabled during the dim time period. |
| `LED`    | `led_count`               | `10`     | Total number of LED's in your WS2811 LED strip                                                                                                                                                                                                                                                                                            |
| `LED`    | `led_freq_hz`             | `800000` | Pulse wavelength frequency for WS2811 LED's. The default (800KHz) should be appropriate in most cases.                                                                                                                                                                                                                                    |
| `LED`    | `led_dma`                 | `10`     | DMA channel for signal generation. The default should be appropriate in most cases.                                                                                                                                                                                                                                                       |
| `LED`    | `led_brightness`          | `255`    | LED brightness, on a scale of 0 (off) to 255 (maximum).                                                                                                                                                                                                                                                                                   |
| `LED`    | `led_invert`              | `false`  | Invert the LED signal (when using NPN transistor level shift)                                                                                                                                                                                                                                                                             |
| `LED`    | `led_channel`             | `0`      | LED output channel (0-2).                                                                                                                                                                                                                                                                                                                 |
| `LED`    | `led_pin`                 | `18`     | Raspberry Pi GPIO Pin for LED control.                                                                                                                                                                                                                                                                                                    |
| `LED`    | `led_rgb_order`           | `rgb`    | Typically color is specific as RGB, but some strips expect GRB. Change this if RGB channels appear swapped.                                                                                                                                                                                                                               |
| `SCREEN` | `airport`                 |          | If provided, this airport will be highlighted on the e-Paper display. Remove to disable.                                                                                                                                                                                                                                                  |

## Usage

```
Usage: metarmap [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  clear   Turn all LED pixels off
  print   Display the most recent METAR for [STATION]
  pulse   Illuminate neopixel at address [PIXEL] for 3 seconds
  update  Update current METAR observation for all airports
```

## License

The content of this project itself is licensed under the [MIT License](LICENSE).

All dependencies used by this project are copyright their respective authors.
