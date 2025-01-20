import logging
from time import time, sleep
import os
import art
from random import shuffle

import config
from modules.conducter import Conducter
from modules.ai_robot_data_writer import AIRobotDataWriter
from modules.biodata_data_writer import BiodataDataWriter
from nebula.hivemind import DataBorg
from nebula.nebula import Nebula
# from modules.rami_main import Rami_Main
from clock import Clock

DATA_LOGGING = config.data_logging
MAIN_PATH = config.path

class Main:
    """
    Main kickstarts the RAMI process. If there is datalogging (Bitalino, Pupil)
    then it will init the connections.
    Essentially, it wil iterate through a series of RAMI experiments, and log
    data for each one separately, while maintaining connection the sensors.
    This is managed through a input question in main_loop.
    """
    def __init__(self):
        # Logging for all modules
        logging.basicConfig(level=logging.WARNING)

        # Build initial dataclass filled with random numbers
        self.hivemind = DataBorg()

        # Init data logging
        if DATA_LOGGING:
            ###################
            # Start Bitalino
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
                    self.eda = BITalino(BITALINO_MAC_ADDRESS)
                    eda_started = True
                except OSError:
                    print("Unable to connect to Bitalino")
                    retry = input("Retry (y/N)? ")
                    if retry.lower() != "y":  #  or retry.lower() != "yes":
                        eda_started = True

            self.eda.start(BITALINO_BAUDRATE, BITALINO_ACQ_CHANNELS)
            first_eda_data = self.eda.read(1)[0]
            logging.info(f'Data from BITalino = {first_eda_data}')

        else:
            self.eda = None

        ###################
        # Start Nebula AI
        ###################
        art.tprint("Wolff1")

        answer = input("Start clock?")

        # Init the AI factory (inherits AIFactory, Listener)
        self.nebula = Nebula(eda=self.eda)  # , speed=config.speed)

        # Init Conducter & Gesture management (controls XArm)
        self.robot = Conducter()

        # Set experiment loop flag
        self.hivemind.MASTER_RUNNING = True

        # self.ui = Clock()
        # self.ui.mainloop()


    def main_loop(self):
        """
        Manage the experiment loop.
        """
        # while self.hivemind.MASTER_RUNNING:
        random_experiment_list = config.experiment_modes
        shuffle(random_experiment_list)
        print("Shuffling experimental modes: ", random_experiment_list)

        for experiment_mode in random_experiment_list:
            while self.hivemind.MASTER_RUNNING:
                # is this first time through with a new experiment
                # if self.ui.go_flag:
                # make new directory for this log e.g. ../data/20240908_123456
                if DATA_LOGGING:
                    self.master_path = f"{MAIN_PATH}/{time()}_mode_{experiment_mode}"
                    self.makenewdir(self.master_path)
                else:
                    self.master_path = None

                # run all systems
                if self.hivemind.running:
                    self.wolff1_main(experiment_mode)

                else:

                    # turn go flag off
                    # self.ui.go_flag = False

                    # if self.hivemind.running:
                    #     self.ui.end_flag = False

                    # update the clock
                    # self.ui.make_clock()
                    sleep(1)
            answer = input("Next Experiment?")

        # end of experiments so close things down
        self.hivemind.MASTER_RUNNING = False
        self.hivemind.running = False

        # close everything like a grown up
        self.terminate_all()

    def terminate_all(self):
        """
        Terminates all active agents and threads
        """
        if DATA_LOGGING:
            self.eda.close()
        self.robot.terminate()
        self.nebula.terminate_listener()

    def wolff1_main(self, experiment_mode):
        """
        Main script to start a single robot arm digital score work.
        Conducter calls the local interpreter for project specific functions. This
        communicates directly to the robot libraries.
        Nebula kick-starts the AI Factory for generating NNet data and affect
        flows.
        This script also controls the live mic audio analyser.
        Paramaters are to be modified in config.py.
        """
        # Init data writer
        if config.data_writer:
            aidw = AIRobotDataWriter(self.master_path)
            bdw = BiodataDataWriter(self.master_path)

        # Start Nebula AI Factory after conducter starts data moving
        self.nebula.endtime = time() + config.duration_of_piece
        self.hivemind.running = True
        # self.robot = Conducter()
        self.robot.main_loop(experiment_mode)
        self.nebula.main_loop()

        if config.data_writer:
            aidw.main_loop()
            bdw.main_loop()

    def makenewdir(self, timestamp):
        try:
            os.makedirs(timestamp)
            print(f"Created dir {timestamp}")
        except OSError:
            print(f"OS Make error. Could not make {timestamp}")


if __name__ == "__main__":
    go = Main()
    go.main_loop()

