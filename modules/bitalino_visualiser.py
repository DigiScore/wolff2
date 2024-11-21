import pandas as pd
import json
import matplotlib.pyplot as plt
# from opensignalsreader import OpenSignalsReader
import neurokit2 as nk
from sklearn.preprocessing import MinMaxScaler
import config

# example of data
# id d1 d2 d3 d4 x y z eda hr bth
# 0	0	0	0	0	494	603	529	684	31	27

class BitalinoVisualiser:

    def __init__(self, raw_file_path, bitalino_images_path):
        # make all variables
        self.figures_path = bitalino_images_path
        self.raw_file_path = raw_file_path
        self.xyz_smoothing_window = 50
        self.sampling_rate = 100
        self.figsize_xy = config.figsize_xy

    # def main(self):

        # load the data from the file
        df = pd.DataFrame(json.loads(open(raw_file_path).read()))

        # each row of x and y is a list; explode the values in the lists to separate rows
        df = df.explode(["date", "x", "y", "z",
                         "eda", "heart", "breath"], ignore_index=True)

        # get date and time
        df["date"] = pd.to_datetime(df["date"])
        date = df["date"]

        # Read OpenSignals file
        # acq = OpenSignalsReader(self.raw_file_path)

        # convert raw data into np arrays
        # x = acq.raw(1)
        # y = acq.raw(2)
        # z = acq.raw(3)
        # eda = acq.raw(4)
        # ecg = acq.raw(5)
        # rsp = acq.raw(6)

        # make into df or numpy
        eda = df["eda"].values
        ecg = df["ecg"].values
        rsp = df["rsp"].values

        x = df["x"]
        y = df["y"]
        z = df["z"]

        # smoothing data
        xs = x.rolling(self.xyz_smoothing_window).sum()
        ys = y.rolling(self.xyz_smoothing_window).sum()
        zs = z.rolling(self.xyz_smoothing_window).sum()

        # Visualise biosignals
        plt.rcParams['figure.figsize'] = self.figsize_xy

        eda_signals, eda_info = nk.eda_process(eda, sampling_rate=self.sampling_rate)
        nk.eda_plot(eda_signals, eda_info)

        ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=self.sampling_rate)
        nk.ecg_plot(ecg_signals, ecg_info)

        rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=self.sampling_rate)
        nk.rsp_plot(rsp_signals, rsp_info)

        plt.show()
        plt.savefig(self.figures_path)

        ##########################
        # Robot movement
        ##########################
        # scale xyz
        scaler = MinMaxScaler(feature_range=(-1, 1))
        xss = scaler.fit_transform(xs)
        yss = scaler.fit_transform(ys)
        zss = scaler.fit_transform(zs)

        # make human xyz plot
        fig, ax = plt.subplots(1, figsize=self.figsize_xy)
        ax.set_title("human xyz")
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Time")
        ax.plot(date, xss, label="x")
        ax.plot(date, yss, label="y")
        ax.plot(date, zss, label="z")
        ax.legend(shadow=True, fancybox=True)

        plt.show()
        plt.savefig(self.figures_path)


if __name__ == "__main__":
    test = BitalinoVisualiser('../data/1732191750.3564394/bitalino/Bitalino_2024_11_21_1222.json',
                              '../data/1732191750.3564394/bitalino/images')
    # test.main()