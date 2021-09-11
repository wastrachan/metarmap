# Basic Metarmap Configuration

I wrote the software for this map to run the one hanging on my own wall, so I didn't invest much time in making it easy to configure.
With that said, configuration should rarely need to be changed, in general this map should be self-sufficient. I've included a couple
of possible scenarios below just in case you need to make a tweak.


### Changing the WiFi Network

1. Remove the SD card from the map. On the back of the map, in the lower-right corner, there is a small circuit board (a Raspberry Pi Zero). This board houses a micro SF card.
2. Plug the SD card into your Mac.
3. You should see a device named `boot` (`/Volumes/boot`) in Finder. Navigate to this device.
4. Open a plaintext editor such as TextEdit and create a new file in this folder. The file must be named `wpa_supplicant.conf`
5. Copy and paste this content into the file, but replace `NETWORK_NAME` with the name of your WiFi network, and replace `PASSWORD` with the password. Make sure that capitalization and spacing in your network name is exact.

        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=US

        network={
            ssid="NETWORK_NAME"
            psk="PASSWORD"
        }

6. Eject the SD card and return it to the map. Boot the map up, and it should connect to the new network automatically.


### Changing the e-Paper Display Airport

The e-paper display will always display the current weather for a single, fixed airport. If you want to change that airport, you can update the configuration file
on the map.

1. Find the IP address of the map. You'll want to look in your router's connected device list for a device named `metarmap`
2. Open the terminal app on your Mac.
3. Type the following command into your terminal to connect to the map. You will need to replace `IP_ADDRESS` with the actual address of the map:

        ssh IP_ADDRESS -lpi

4. You will be asked for a password. Enter the password `metarmap`. The characters will not display as you type. Press "enter" when you are finished- you will be shown a prompt after logging in that resembles `pi@metarmap:~ $`
5. Open the configuration file with the following command:

        sudo nano /root/.config/metarmap/config

6. You will be presented with a text-based editor. Using your arrow keys, navigate to the `SCREEN` section. Replace the airport identifier here with the new airport you would like to display on the e-paper display.

        [SCREEN]
        airport = KRYY

7. When you are finished, press "CTRL+X". The editor will ask you if you want to save your changes. Press "y". The editor will ask you what you would like to name the file. Press "enter" without making any other changes.
8. Type the word `exit` in the prompt, and press "enter". Close the terminal app on your Mac.
9. The next time the map updates (every ten minutes) the display will refresh to reflect the new airport you have configured.


### Update the Metarmap Software

You will not need to update the software on the map unless I have to fix a bug in the future (maybe the FAA begins to return weather data in a new format). In this scenario, I'll probably let you know personally that you need to update the software to fix the issue. In any other case, this procedure won't be necessary.

1. Find the IP address of the map. You'll want to look in your router's connected device list for a device named `metarmap`
2. Open the terminal app on your Mac.
3. Type the following command into your terminal to connect to the map. You will need to replace `IP_ADDRESS` with the actual address of the map:

        ssh IP_ADDRESS -lpi

4. You will be asked for a password. Enter the password `metarmap`. The characters will not display as you type. Press "enter" when you are finished- you will be shown a prompt after logging in that resembles `pi@metarmap:~ $`

5. Enter the following command exactly as written to perform the update:

        cd metarmap; git pull; sudo pip3 install .

6. The command will run for several minutes. When it finishes, you will once again see the prompt: `pi@metarmap:~ $`
7. Type the word `exit` in the prompt, and press "enter". Close the terminal app on your Mac.
