from modules.listener import Listener
from nebula.hivemind import DataBorg
import logging
logging.basicConfig(level=logging.DEBUG)

db = DataBorg()

listener = Listener()
listener.hivemind.running = True
listener.snd_listen()
