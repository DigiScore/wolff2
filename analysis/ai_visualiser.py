import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# example of data
# {"date": "2024-06-19T09:23:53.715722", "master_stream": "mic_in", "mic_in": 0.19192041015625, "rnd_poetry": 0.4705154363470828, "flow2core": 0.4325794083715225, "core2flow": 0.6366659559974667, "audio2core": 0.15154093505951877, "audio2flow": 0.4944602665519162, "flow2audio": 2.256709656255868e-07, "eda2flow": 0.9999999793856779, "current_robot_x_y_z": {"x": 0, "y": 0, "z": 0, "design decision": " ", "interrupt": false}},


# load the data from the file
df = pd.read_json('../data/2024_11_05_1233.json')
# print(df.head())

robot = pd.json_normalize(df["current_robot_x_y_z"])
# interrupt = str(robot["interrupt"])

# each row of x and y is a list; explode the values in the lists to separate rows
df = df.explode(["date", "master_stream", "mic_in", "rnd_poetry", "flow2core", "core2flow",
                 "audio2core", "audio2flow", "flow2audio", "eda2flow"], ignore_index=True)

df["date"] = pd.to_datetime(df["date"])
date = df["date"]
# the easiest option is to use seaborn, which is an api for matplotlib
# sns.relplot(kind='line', data=df, x="date", y="master_stream", marker='.')
# sns.relplot(kind='line', data=df, x="date", y="mic_in", marker='.')
fig, ax = plt.subplots(3, figsize=(60, 6))
ax[0].plot(date, df["mic_in"])
ax[0].plot(date, df["rnd_poetry"])
ax[0].plot(date, df["flow2core"])
ax[0].plot(date, df["core2flow"])
ax[0].plot(date, df["audio2core"])
ax[0].plot(date, df["audio2flow"])
ax[0].plot(date, df["flow2audio"])
ax[0].plot(date, df["eda2flow"])

ax[1].plot(date, df["master_stream"])
# ax[1].plot(date, interrupt)

ax[2].plot(date, robot["x"])
ax[2].plot(date, robot["y"])
ax[2].plot(date, robot["z"])

plt.show()
