import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk


x_path = "../data/2024-11-15_12-02-42-015496_MX.csv"
y_path = "../data/2024-11-15_12-02-42-015496_MY.csv"
z_path = "../data/2024-11-15_12-02-42-015496_MZ.csv"

x_df = pd.read_csv(x_path)
y_df = pd.read_csv(y_path)
z_df = pd.read_csv(z_path)
# print(eda_df.head())

x_df = x_df.explode(
    [
        "LocalTimestamp",
        "EmotiBitTimestamp",
        "PacketNumber",
        "DataLength",
        "TypeTag",
        "ProtocolVersion",
        "DataReliability",
        "MX",
    ],
    ignore_index=True,
)
y_df = y_df.explode(
    [
        "LocalTimestamp",
        "EmotiBitTimestamp",
        "PacketNumber",
        "DataLength",
        "TypeTag",
        "ProtocolVersion",
        "DataReliability",
        "MY",
    ],
    ignore_index=True,
)
z_df = z_df.explode(
    [
        "LocalTimestamp",
        "EmotiBitTimestamp",
        "PacketNumber",
        "DataLength",
        "TypeTag",
        "ProtocolVersion",
        "DataReliability",
        "MZ",
    ],
    ignore_index=True,
)


# get date and time
x_df["date"] = pd.to_datetime(x_df["LocalTimestamp"])
date = x_df["date"]

# make master plot
fig, ax = plt.subplots(1, figsize=(60, 12))


# # plot EDA
# ax[0].plot(date, eda_df["EA"], label="EDA")
xs = x_df["MX"]  # .rolling(10).sum()
ys = y_df["MY"]  # .rolling(10).sum()
zs = z_df["MZ"]  # .rolling(10).sum()

# plot robot xyz
ax.set_title("Robot xyz")
ax.set_ylabel("Amplitude")
ax.set_xlabel("Time")
ax.plot(date, xs, label="x")
ax.plot(date, ys, label="y")
ax.plot(date, zs, label="z")
ax.legend(shadow=True, fancybox=True)


# eda_path = "../data/2024-11-15_12-02-42-015496_EA.csv"
# sa_path = "../data/2024-11-15_12-02-42-015496_SA.csv"
# sf_path = "../data/2024-11-15_12-02-42-015496_SF.csv"
# sr_path = "../data/2024-11-15_12-02-42-015496_SR.csv"
#
# eda_df = pd.read_csv(eda_path)
# sa_df = pd.read_csv(sa_path)
# sf_df = pd.read_csv(sf_path)
# sr_df = pd.read_csv(sr_path)
# # print(eda_df.head())
#
# eda_df = eda_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "EA"], ignore_index=True)
# sa_df = sa_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "SA"], ignore_index=True)
# sf_df = sf_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "SF"], ignore_index=True)
# sr_df = sr_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "SR"], ignore_index=True)
#
# eda_signals, eda_info = nk.eda_process(eda_df["EA"], sampling_rate=25)
# nk.eda_plot(eda_signals, eda_info)


#
# # get date and time
# eda_df["date"] = pd.to_datetime(eda_df["LocalTimestamp"])
# date = eda_df["date"]
#
# print("lengths", len(eda_df["date"]), len(sr_df["SR"]))
#
#
# # make master plot
# fig, ax = plt.subplots(4, figsize=(60, 12))
#
# # plot EDA
# ax[0].plot(date, eda_df["EA"], label="EDA")
#
#
# ax[0].set_title("EDA")
# ax[0].set_ylabel("Amplitude")
# ax[0].set_xlabel("Time")
#
# ax[1].plot(sa_df["LocalTimestamp"], sa_df["SA"], label="SA")
# ax[2].plot(sf_df["LocalTimestamp"], sf_df["SF"], label="SF")
# ax[3].plot(sr_df["LocalTimestamp"], sr_df["SR"], label="SR")
#

# hr_path = "../data/2024-11-15_12-02-42-015496_HR.csv"
# bi_path = "../data/2024-11-15_12-02-42-015496_BI.csv"
#
# hr_df = pd.read_csv(hr_path)
# bi_df = pd.read_csv(bi_path)
#
# # print(eda_df.head())
#
# hr_df = hr_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "HR"], ignore_index=True)
# bi_df = bi_df.explode(["LocalTimestamp", "EmotiBitTimestamp", "PacketNumber", "DataLength",
#                  "TypeTag", "ProtocolVersion", "DataReliability", "BI"], ignore_index=True)
#
# ecg_signals, ecg_info = nk.ecg_process(bi_df["BI"], sampling_rate=25)
# nk.ecg_plot(ecg_signals, ecg_info)
#
#
# # get date and time
# hr_df["date"] = pd.to_datetime(hr_df["LocalTimestamp"])
# date = hr_df["date"]
#
# # print("lengths", len(eda_df["date"]), len(sr_df["SR"]))
#
#
# # make master plot
# fig, ax = plt.subplots(2, figsize=(60, 12))
#
# # plot EDA
# ax[0].plot(date, hr_df["HR"], label="HR")
# ax[0].legend(shadow=True, fancybox=True)
#
#
# # ax[0].set_title("EDA")
# # ax[0].set_ylabel("Amplitude")
# # ax[0].set_xlabel("Time")
#
# ax[1].plot(date, bi_df["BI"], label="Beat Interval")
# ax[1].legend(shadow=True, fancybox=True)


plt.show()
