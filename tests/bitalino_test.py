from time import time
import config
from modules.biodata_data_writer import BiodataDataWriter
from modules.bitalino import BITalino
from nebula.hivemind import DataBorg



# make new directory for this log e.g. ../data/20240908_123456
master_path = f"../data/{time()}"
hivemind = DataBorg()
###################
# Bitalino
###################
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
first_eda_data = "hiya"  #eda.read(1)[0]
print(f'Data from BITalino = {first_eda_data}')


hivemind.running = True



test = BiodataDataWriter(master_path)
test._test_running()
test.main_loop()
