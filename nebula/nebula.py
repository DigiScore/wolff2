"""
Embodied AI Engine Prototype AKA "Nebula". This object takes a live signal
(such as body tracking, or real-time sound analysis) and generates a response
that aims to be felt as co-creative. The response is a flow of neural network
emissions data packaged as a dictionary, and is gestural over time. This, when
plugged into a responding script (such as a sound generator, or QT graphics)
gives the feeling of the AI creating in-the-moment with the human in-the-loop.

© Craig Vear 2022-24
craig.vear@nottingham.ac.uk

Dedicated to Fabrizio Poltronieri
"""

import logging
import numpy as np
import warnings
from scipy import signal
from threading import Thread
from time import sleep, time

from sympy import false

import config
from modules import bitalino_module

# from modules.brainbit import BrainbitReader
from modules.listener import Listener
from nebula.ai_factory import AIFactoryRAMI


def scaler(in_feature, mins, maxs):
    """
    Min-max scaler with clipping.
    """
    warnings.filterwarnings("error")
    in_feature = np.array(in_feature)
    mins = np.array(mins)
    maxs = np.array(maxs)
    try:
        norm_feature = (in_feature - mins) / (maxs - mins)
    except RuntimeWarning:
        logging.info("Scaler encountered zero division")
        norm_feature = in_feature
    norm_feature = norm_feature.clip(0, 1)
    warnings.simplefilter("always")
    return norm_feature


class Nebula(Listener, AIFactoryRAMI):
    """
    Nebula is the core "director" of an AI factory. It generates data in
    response to incoming percepts from human-in-the-loop interactions, and
    responds in-the-moment to the gestural input of live data.
    There are 4 components:
        - Nebula: as "director" it coordinates the overall operations of the AI
        Factory.
        - AIFactory: builds the neural nets that form the factory, coordinates
        data exchange, and liases with the common data dict.
        - Hivemind: is the central dataclass that holds and shares all the data
        exchanges in the AI factory.
        - Conducter: receives the live percept input from the client and
        produces an affectual response to it's energy input, which in turn
        interferes with the data generation.
    """

    def __init__(self, eda):  # , speed=1):
        """
        Parameters
        ----------
        speed
            General tempo/ feel of Nebula's response (0.5 ~ moderate fast,
            1 ~ moderato, 2 ~ presto).
        """
        warnings.simplefilter("ignore")
        print("Building engine server")
        Listener.__init__(self)

        # Set global vars
        # self.hivemind.running = True

        # Build the AI factory and pass it the data dict
        AIFactoryRAMI.__init__(self)  # , speed)

        # Own Bitalino
        self.BITALINO_CONNECTED = config.data_logging
        if self.BITALINO_CONNECTED:
            self.eda = eda

        # Work out master timing then collapse hivemind.running
        self.endtime = 0

        self.bitalino_on = True

    def main_loop(self):
        """
        Starts the server / AI threads and gets the data rolling.
        """
        print("Starting the Nebula director")
        # Declare all threads
        t1 = Thread(target=self.make_data)
        t2 = Thread(target=self.snd_listen)
        t3 = Thread(target=self.human_input)
        t4 = Thread(target=self.restart_bitalino)

        # Start them all
        t1.start()
        t2.start()
        t3.start()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            t4.start()

    def restart_bitalino(self):
        warnings.simplefilter("ignore")
        while True:
            sleep(120)
            self.bitalino_on = False
            with warnings.catch_warnings():
                try:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    self.eda.stop()
                    self.eda.close()
                except OSError:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    ...
                bitalino_ok = false
                while not bitalino_ok:
                    try:
                        warnings.filterwarnings("ignore", category=DeprecationWarning)
                        self.eda = bitalino_module.BITalino(config.mac_address)
                        bitalino_ok = True
                    except OSError:
                        warnings.filterwarnings("ignore", category=DeprecationWarning)
                        ...
                try:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    self.eda.start(config.baudrate, config.channels)
                    self.bitalino_on = True
                except OSError:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    ...


    def human_input(self):
        """
        Listen to live human input.
        """
        while self.hivemind.running:
            if time() >= self.endtime:
                break
            # Read data from bitalino
            if self.BITALINO_CONNECTED and self.bitalino_on:
                try:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    # Get raw data from Bitalino
                    bitalino_raw = self.eda.read(1)[0]

                    # write out the Bitalino data to the log
                    self.hivemind.bitalino_x = int(bitalino_raw[5])

                    self.hivemind.bitalino_y = int(bitalino_raw[6])

                    self.hivemind.bitalino_z = int(bitalino_raw[7])

                    self.hivemind.bitalino_eda = int(bitalino_raw[8])

                    # self.hivemind.bitalino_ecg = int(bitalino_raw[9])
                    #
                    # self.hivemind.bitalino_rsp = int(bitalino_raw[10])

                    # extract eda for processing
                    eda_raw = [self.hivemind.bitalino_eda]  # [self.eda.read(1)[0][-1]]

                    logging.debug(f"eda data raw = {eda_raw}")

                    # Update raw EDA buffer
                    eda_2d = np.array(eda_raw)[:, np.newaxis]
                    self.hivemind.eda_buffer_raw = np.append(
                        self.hivemind.eda_buffer_raw, eda_2d, axis=1
                    )
                    self.hivemind.eda_buffer_raw = np.delete(
                        self.hivemind.eda_buffer_raw, 0, axis=1
                    )

                    # Detrend on the buffer time window
                    eda_detrend = signal.detrend(self.hivemind.eda_buffer_raw)

                    # Get min and max from raw EDA buffer
                    eda_mins = np.min(eda_detrend, axis=1)
                    eda_maxs = np.max(eda_detrend, axis=1)
                    eda_mins = eda_mins - 0.05 * (eda_maxs - eda_mins)

                    # Rescale between 0 and 1
                    eda_norm = scaler(eda_detrend[:, -1], eda_mins, eda_maxs)

                    # Update normalised EDA buffer
                    eda_2d = eda_norm[:, np.newaxis]
                    self.hivemind.eda_buffer = np.append(
                        self.hivemind.eda_buffer, eda_2d, axis=1
                    )
                    self.hivemind.eda_buffer = np.delete(
                        self.hivemind.eda_buffer, 0, axis=1
                    )
                except OSError:
                    try:
                        with warnings.catch_warnings():
                            self.hivemind.eda_buffer = np.random.uniform(size=(1, 50))
                            warnings.filterwarnings("ignore", category=DeprecationWarning)
                            self.eda.stop()
                            self.eda.close()
                            self.eda.start(config.baudrate, config.channels)
                    except OSError:
                        ...
            else:
                # Random data if no bitalino
                self.hivemind.eda_buffer = np.random.uniform(size=(1, 50))

            sleep(0.01)  # for 100 Hz

        self.hivemind.running = False
        # self.hivemind.MASTER_RUNNING = False

    # def terminate(self):
    #     """
    #     Terminate threads and connections like a grownup.
    #     """
    #     if self.BITALINO_CONNECTED:
    #         self.eda.close()
