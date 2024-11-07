import config
import logging

import rami_main
from modules.bitalino import BITalino
from rami_main import Rami_Main

BITALINO_CONNECTED = config.eda_live


def main():

    # Init bitalino
    if BITALINO_CONNECTED:
        BITALINO_MAC_ADDRESS = config.mac_address
        BITALINO_BAUDRATE = config.baudrate
        BITALINO_ACQ_CHANNELS = config.channels

        eda_started = False
        while not eda_started:
            try:
                eda = BITalino(BITALINO_MAC_ADDRESS)
                eda_started = True
            except OSError:
                print("Unable to connect to Bitalino")
                retry = input("Retry (y/N)? ")
                if retry.lower() != "y" and retry.lower() != "yes":
                    eda_started = True

        eda.start(BITALINO_BAUDRATE, BITALINO_ACQ_CHANNELS)
        first_eda_data = eda.read(1)[0]
        logging.info(f'Data from BITalino = {first_eda_data}')

    else:
        eda = None

    while True:
        rami = Rami_Main(eda)


    if BITALINO_CONNECTED:
        eda.close()