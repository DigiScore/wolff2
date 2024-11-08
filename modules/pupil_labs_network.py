import zmq
import config

class PupilLabs:
    PUPIL_LABS_ADDR = config.pupil_labs_addr

    def __init__(self):

        # pupil_labs_started = False
        ctx = zmq.Context()
        self.socket = zmq.Socket(ctx, zmq.REQ)
        self.socket.connect(self.PUPIL_LABS_ADDR)
        # while not pupil_labs_started:
        #     try:
        #         self.socket.send_string("test")
        #     except:
        #         pass
        #     finally:
        #         pupil_labs_started = True

    def start_record(self):
        self.socket.send_string("R")
        print(self.socket.recv_string())

    def stop_record(self):
            self.socket.send_string("r")
            print(self.socket.recv_string())
