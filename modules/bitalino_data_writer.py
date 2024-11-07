import json
import logging
import os
from datetime import datetime
from threading import Thread
from time import sleep

from nebula.hivemind import DataBorg


class BitalinoDataWriter:

    def __init__(self):
        self.hivemind = DataBorg()
        self.data_file = open(f"data/Bitalino_{self.hivemind.session_date}.json", "a")
        self.data_file.write("[")

    def json_update(self):
        """
        Write a hiveming tic in the json file.
        """
        json_dict = {
            "date": datetime.now().isoformat(),
            "x": self.hivemind.bitalino_x,
            "y": self.hivemind.bitalino_y,
            "z": self.hivemind.bitalino_z,
            "eda": self.hivemind.bitalino_eda,
            "heart": self.hivemind.bitalino_heart,
            "breath": self.hivemind.bitalino_breath,
            "button": self.hivemind.bitalino_button
        }
        json_object = json.dumps(json_dict)
        self.data_file.write(json_object)
        self.data_file.write(',\n')

    def terminate_data_writer(self):
        """
        Terminate the json writer and close file.
        """
        self.data_file.seek(self.data_file.tell() - 3, os.SEEK_SET)
        self.data_file.truncate()  # remove ",\n"
        self.data_file.write("]")
        self.data_file.close()

    def main_loop(self):
        """
        Start the main thread for the writing manager.
        """
        writer_thread = Thread(target=self.writing_manager)
        writer_thread.start()

    def writing_manager(self):
        """
        Write realtime data from hivemind.
        """
        while self.hivemind.running:
            self.json_update()
            sleep(0.01)
        logging.info("quitting data writer thread")
        self.terminate_data_writer()
