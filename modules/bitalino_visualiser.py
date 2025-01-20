import pandas as pd
import json
import matplotlib.pyplot as plt
import neurokit2 as nk
from neurokit2 import NeuroKitWarning
from neurokit2.signal.signal_rate import _signal_rate_plot
from neurokit2.ecg.ecg_peaks import _ecg_peaks_plot
from sklearn.preprocessing import MinMaxScaler
from warnings import warn
import matplotlib.gridspec
import numpy as np

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

        # load the data from the file
        df = pd.DataFrame(json.loads(open(raw_file_path).read()))

        # each row of x and y is a list; explode the values in the lists to separate rows
        df = df.explode(["date", "x", "y", "z",
                         "eda"], ignore_index=True)

        # get date and time
        df["date"] = pd.to_datetime(df["date"])
        date = df["date"]

        # Read data file make into df or numpy
        eda = df["eda"].values
        # ecg = df["ecg"].values
        # rsp = df["rsp"].values

        x = pd.DataFrame(df["x"])
        y = pd.DataFrame(df["y"])
        z = pd.DataFrame(df["z"])

        # smoothing data
        xs = x.rolling(self.xyz_smoothing_window).sum()
        ys = y.rolling(self.xyz_smoothing_window).sum()
        zs = z.rolling(self.xyz_smoothing_window).sum()

        # Visualise biosignals
        plt.rcParams['figure.figsize'] = self.figsize_xy

        eda_signals, eda_info = nk.eda_process(eda, sampling_rate=self.sampling_rate)
        nk.eda_plot(eda_signals, eda_info)
        plt.savefig(f"{self.figures_path}/eda")

        # ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=self.sampling_rate)
        # self.rami_ecg_plot(ecg_signals, ecg_info)
        # plt.savefig(f"{self.figures_path}/ecg")
        #
        # rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=self.sampling_rate)
        # nk.rsp_plot(rsp_signals, rsp_info)
        # plt.savefig(f"{self.figures_path}/rsp")

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

        # plt.show()
        plt.savefig(f"{self.figures_path}/xyz")

    def rami_ecg_plot(self, ecg_signals, info=None):
        """**Visualize ECG data**

        Plot ECG signals and R-peaks.

        Parameters
        ----------
        ecg_signals : DataFrame
            DataFrame obtained from ``ecg_process()``.
        info : dict
            The information Dict returned by ``ecg_process()``. Defaults to ``None``.

        See Also
        --------
        ecg_process

        Returns
        -------
        Though the function returns nothing, the figure can be retrieved and saved as follows:

        .. code-block:: python

          # To be run after ecg_plot()
          fig = plt.gcf()
          fig.set_size_inches(10, 12, forward=True)
          fig.savefig("myfig.png")

        Examples
        --------
        .. ipython:: python

          import neurokit2 as nk

          # Simulate data
          ecg = nk.ecg_simulate(duration=15, sampling_rate=1000, heart_rate=80)

          # Process signal
          signals, info = nk.ecg_process(ecg, sampling_rate=1000)

          # Plot
          @savefig p_ecg_plot.png scale=100%
          nk.ecg_plot(signals, info)
          @suppress
          plt.close()

        """
        # Sanity-check input.
        if not isinstance(ecg_signals, pd.DataFrame):
            raise ValueError(
                "NeuroKit error: ecg_plot(): The `ecg_signals` argument must be the "
                "DataFrame returned by `ecg_process()`."
            )

        # Extract R-peaks.
        if info is None:
            warn(
                "'info' dict not provided. Some information might be missing."
                + " Sampling rate will be set to 1000 Hz.",
                category=NeuroKitWarning,
            )
            info = {"sampling_rate": 1000}

        # Extract R-peaks (take those from df as it might have been cropped)
        if "ECG_R_Peaks" in ecg_signals.columns:
            info["ECG_R_Peaks"] = np.where(ecg_signals["ECG_R_Peaks"] == 1)[0]

        # Prepare figure and set axes.
        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[2 / 3, 1 / 3])

        fig = plt.figure(constrained_layout=False)
        fig.suptitle("Electrocardiogram (ECG)", fontweight="bold")

        ax0 = fig.add_subplot(gs[0, :])
        ax1 = fig.add_subplot(gs[1, :], sharex=ax0)
        # ax2 = fig.add_subplot(gs[:, -1])

        # Plot signals
        phase = None
        if "ECG_Phase_Ventricular" in ecg_signals.columns:
            phase = ecg_signals["ECG_Phase_Ventricular"].values

        ax0 = _ecg_peaks_plot(
            ecg_signals["ECG_Clean"].values,
            info=info,
            sampling_rate=info["sampling_rate"],
            raw=ecg_signals["ECG_Raw"].values,
            quality=ecg_signals["ECG_Quality"].values,
            phase=phase,
            ax=ax0,
        )

        # Plot Heart Rate
        ax1 = _signal_rate_plot(
            ecg_signals["ECG_Rate"].values,
            info["ECG_R_Peaks"],
            sampling_rate=info["sampling_rate"],
            title="Heart Rate",
            ytitle="Beats per minute (bpm)",
            color="#FF5722",
            color_mean="#FF9800",
            color_points="#FFC107",
            ax=ax1,
        )

if __name__ == "__main__":
    test = BitalinoVisualiser('../data/1732271846.9152355/bitalino/Bitalino_2024_11_22_1037.json',
                              '../data/1732271846.9152355/bitalino/images')
