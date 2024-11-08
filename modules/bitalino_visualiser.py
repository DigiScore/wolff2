# import pandas as pd
# import numpy as np
# from pandas import HDFStore
import matplotlib.pyplot as plt
# Import OpenSignalsReader
from opensignalsreader import OpenSignalsReader
import neurokit2 as nk



# example of data
# id d1 d2 d3 d4 x y z eda hr bth
# 0	0	0	0	0	494	603	529	684	31	27

path = '../data/opensignals_98d3b1fd3d1f_2024-11-05_10-42-51.txt'


#


plt.rcParams['figure.figsize'] = [60, 12]
# Read OpenSignals file
acq = OpenSignalsReader(path)

# convert raw data into np arrays
# x = pd.DataFrame(acq.raw(1))
# y = pd.DataFrame(acq.raw(2))
# z = pd.DataFrame(acq.raw(3))
eda = acq.raw(4)
ecg = acq.raw(5)
rsp = acq.raw(6)

# chop raw data to fit size
eda = eda[62000:75000]
ecg = ecg[62000:75000]
rsp = rsp[62000:75000]

# Visualise biosignals
eda_signals, eda_info = nk.eda_process(eda, sampling_rate=100)
nk.eda_plot(eda_signals, eda_info)

ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=100)
nk.ecg_plot(ecg_signals, ecg_info)

rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=100)
nk.rsp_plot(rsp_signals, rsp_info)


plt.show()

#
#
# class Biodata_visualiser:
#
#     def __init__(self, path):
#         self.path = path
#
#
#         plt.savefig(path)
#
# if __name__ == "__main__":
#     test = AI_visualiser(path='../data/2024_11_05_1233.json')
