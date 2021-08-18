import configparser
import os

HOME_DIR = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME_DIR, '.config/metarmap')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config')

config = configparser.ConfigParser()


def setup_configuration():
    """ Create a default configuration file at ~/.config/metarmap/config
    if no existing configuration file can be found
    """
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    # Load configuration
    config.read(CONFIG_FILE)
    rewrite_config = False

    # Ensure top-level sections exist
    if 'LED' not in config.sections():
        rewrite_config = True
        config['LED'] = {}

    if 'AIRPORTS' not in config.sections():
        rewrite_config = True
        config['AIRPORTS'] = {
            '1': 'KRYY'
        }

    # Ensure minimum config options in LED section
    led = config['LED']
    if not led.get('LED_COUNT'):
        rewrite_config = True
        led['LED_COUNT'] = '50'
    if not led.get('LED_COUNT'):
        rewrite_config = True
        led['LED_PIN'] = '18'
    if not led.get('LED_FREQ_HZ'):
        rewrite_config = True
        led['LED_FREQ_HZ'] = '800000'
    if not led.get('LED_DMA'):
        rewrite_config = True
        led['LED_DMA'] = '10'
    if not led.get('LED_BRIGHTNESS'):
        rewrite_config = True
        led['LED_BRIGHTNESS'] = '255'
    if not led.get('LED_INVERT'):
        rewrite_config = True
        led['LED_INVERT'] = 'false'
    if not led.get('LED_CHANNEL'):
        rewrite_config = True
        led['LED_CHANNEL'] = '0'

    # Save configuration defaults
    if rewrite_config:
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
