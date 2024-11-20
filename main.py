import config
import logging
from time import time
import os

from modules.rami_main import Rami_Main

DATA_LOGGING = config.data_logging
MAIN_PATH = config.path

class Main:
    def __init__(self):
        # Init data logging
        if DATA_LOGGING:
            # make new directory for this log e.g. ../data/20240908_123456
            master_path = f"{MAIN_PATH}/{time()}"
            self.makenewdir(master_path)

            ###################
            # Bitalino
            ###################
            # get relevant libraries
            from modules.bitalino import BITalino

            # start bitalino
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
            input('To start press ENTER')

            rami = Rami_Main(eda, master_path)


        # if BITALINO_CONNECTED:
        #     eda.close()


    def makenewdir(self, timestamp):
        try:
            os.makedirs(timestamp)
            print(f"Created dir {timestamp}")
        except OSError:
            print("error")
        # let exception propagate if we just can't
        # cd into the specified directory
        # os.chdir(timestamp)


if __name__ == "__main__":
    Main()
