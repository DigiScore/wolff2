import bitalino
import numpy
import time

from config import mac_address

print(mac_address)

device = bitalino.BITalino(mac_address)
time.sleep(1)

srate = 1000
nframes = 100
thresold = 5

device.start(srate, [0])
print("START")

try:
    while True:
        data = device.read(nframes)

        device.started

        if numpy.mean(data[:, 1]) < 1 : break

        EMG = data[:, -1]

        envelope = numpy.abs(numpy.diff(EMG))

        if envelope > thresold:
            device.trigger([0, 1])
        else:
            device.trigger([0, 0])

finally:
    print("STOP")
    device.trigger([0, 0])
    device.stop()
    device.close()
