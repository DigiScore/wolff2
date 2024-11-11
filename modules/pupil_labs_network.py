import os
import zmq
import config
from threading import Thread
from modules.pupil_labs_visualiser import PupilLabsVisualiser

class PupilLabs:
    """https://github.com/pupil-labs/pupil-helpers/blob/master/python/pupil_remote_control.py
    """
    PUPIL_LABS_ADDR = config.pupil_labs_addr

    def __init__(self, master_path):

        # pupil_labs_started = False
        ctx = zmq.Context()
        self.socket = zmq.Socket(ctx, zmq.REQ)
        self.socket.connect(self.PUPIL_LABS_ADDR)

        # todo - check its connected!!
        # while not pupil_labs_started:
        #     try:
        #         self.socket.send_string("test")
        #     except:
        #         pass
        #     finally:
        #         pupil_labs_started = True

        # get visualiser ready
        # todo create folders
        self.pupillabs_path = f"{master_path}/pupilLabs"
        self.makenewdir(self.pupillabs_path)

    def start_record(self):
        self.socket.send_string("R")
        print(self.socket.recv_string())

    def stop_record(self):
            self.socket.send_string("r")
            print(self.socket.recv_string())

    def process_data(self):
        self.pupil_vis = PupilLabsVisualiser(self.pupillabs_path)
        pupil_thread = Thread(target=self._process_data)
        pupil_thread.start()

    def _process_data(self):
        self.pupil_vis.main()

    def makenewdir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            print(f"Path Error - unable to create Directory {path}")

