import json
import logging
import os
from datetime import datetime
from threading import Thread
from time import sleep, time
from pathlib import Path

from nebula.hivemind import DataBorg
from modules.bitalino_visualiser import BitalinoVisualiser
# from modules.pupil_labs_network import PupilLabs
import config


class BiodataDataWriter:

    def __init__(self, master_path):
        # make all dirs for data logging
        self.bitalino_path = Path(f"{master_path}/bitalino")
        self.makenewdir(self.bitalino_path)

        self.bitalino_images = Path(f"{self.bitalino_path}/images")
        self.makenewdir(self.bitalino_images)

        self.hivemind = DataBorg()
        self.samplerate = config.samplerate

        self.data_file_path = Path(f"{self.bitalino_path}/Bitalino_{self.hivemind.session_date}.json")
        self.data_file = open(self.data_file_path, "a")
        self.data_file.write("[")

        ###################
        # init pupil labs
        ###################
        # if config.pupil_logging:
        #     self.pupil_labs = PupilLabs(master_path)

    def json_update(self):
        """
        Write a hivemind tic in the json file.
        """
        json_dict = {
            "date": datetime.now().isoformat(),
            "x": self.hivemind.bitalino_x,
            "y": self.hivemind.bitalino_y,
            "z": self.hivemind.bitalino_z,
            "eda": self.hivemind.bitalino_eda,
            # "ecg": self.hivemind.bitalino_ecg,
            # "rsp": self.hivemind.bitalino_rsp,
            # "button": self.hivemind.bitalino_button,
        }
        json_object = json.dumps(json_dict)
        self.data_file.write(json_object)
        self.data_file.write(',\n')

    def terminate_data_writer(self):
        """
        Terminate the json writer and close file.
        """
        ###################
        # init pupil labs
        ###################
        # close pupil labs
        # if config.pupil_logging:
        #     self.pupil_labs.stop_record()

        # close bitalino
        self.data_file.seek(self.data_file.tell() - 3, os.SEEK_SET)
        self.data_file.truncate()  # remove ",\n"
        self.data_file.write("]")
        self.data_file.close()
        # sleep(3)
        # self.process_data()

    def main_loop(self):
        """
        Start the main thread for the writing manager.
        """
        # if config.pupil_logging:
        #     self.pupil_labs.start_record()
        writer_thread = Thread(target=self.writing_manager)
        writer_thread.start()

    def writing_manager(self):
        """
        Write realtime data from hivemind.
        """
        while self.hivemind.running:
            self.json_update()
            sleep(self.samplerate)
        logging.info("quitting data writer thread")
        self.terminate_data_writer()

    def process_data(self):
        visualiser = BitalinoVisualiser(self.data_file_path, self.bitalino_images)

    def makenewdir(self, path):
        try:
            path.mkdir(parents=True)
            # os.mkdir(path)
        except OSError:
            print(f"Path Error - unable to create Directory {path} as it might already exist.")

    def _test_running(self):
        self.hivemind.running = True


