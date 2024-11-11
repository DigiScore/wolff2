import pandas as pd

import matplotlib.pyplot as plt
from opensignalsreader import OpenSignalsReader
import neurokit2 as nk
from sklearn.preprocessing import MinMaxScaler

# example of data
# id d1 d2 d3 d4 x y z eda hr bth
# 0	0	0	0	0	494	603	529	684	31	27

path = '../data/opensignals_98d3b1fd3d1f_2024-11-05_10-42-51.txt'

xyz_smoothing_window = 50
sampling_rate = 100
figsize_xy = (60, 12)

# Read OpenSignals file
acq = OpenSignalsReader(path)

# convert raw data into np arrays
x = acq.raw(1)
y = acq.raw(2)
z = acq.raw(3)
eda = acq.raw(4)
ecg = acq.raw(5)
rsp = acq.raw(6)

# chop raw data to fit size
# x = x[62000:75000]
# y = y[62000:75000]
# z = z[62000:75000]
# eda = eda[62000:75000]
# ecg = ecg[62000:75000]
# rsp = rsp[62000:75000]

# make into pandas df
x = pd.DataFrame(x)
y = pd.DataFrame(y)
z = pd.DataFrame(z)

xs = x.rolling(xyz_smoothing_window).sum()
ys = y.rolling(xyz_smoothing_window).sum()
zs = z.rolling(xyz_smoothing_window).sum()


# Visualise biosignals
plt.rcParams['figure.figsize'] = figsize_xy

eda_signals, eda_info = nk.eda_process(eda, sampling_rate=sampling_rate)
nk.eda_plot(eda_signals, eda_info)

ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=sampling_rate)
nk.ecg_plot(ecg_signals, ecg_info)

rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=sampling_rate)
nk.rsp_plot(rsp_signals, rsp_info)


plt.show()



##########################
# Robot movement
##########################
# scale xyz
scaler = MinMaxScaler(feature_range=(-1, 1))
xss = scaler.fit_transform(xs)
yss = scaler.fit_transform(ys)
zss = scaler.fit_transform(zs)

# make human xyz plot
fig, ax = plt.subplots(1, figsize=figsize_xy)
ax.set_title("human xyz")
ax.set_ylabel("Amplitude")
ax.set_xlabel("Time")
ax.plot(x.index, xss, label="x")
ax.plot(y.index, yss, label="y")
ax.plot(z.index, zss, label="z")
ax.legend(shadow=True, fancybox=True)

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
