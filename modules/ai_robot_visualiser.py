import pandas as pd
import matplotlib.pyplot as plt
import config

# example of data
# {"date": "2024-06-19T09:23:53.715722", "master_stream": "mic_in", "mic_in": 0.19192041015625, "rnd_poetry": 0.4705154363470828, "flow2core": 0.4325794083715225, "core2flow": 0.6366659559974667, "audio2core": 0.15154093505951877, "audio2flow": 0.4944602665519162, "flow2audio": 2.256709656255868e-07, "eda2flow": 0.9999999793856779, "current_robot_x_y_z": {"x": 0, "y": 0, "z": 0, "design decision": " ", "interrupt": false}},

class AI_visualiser:

    def __init__(self, raw_file_path, ai_robot__images_path):
        # variables
        self.ai_robot__images_path = ai_robot__images_path
        self.figsize_xy = config.figsize_xy

        # load the data from the file
        df = pd.read_json(raw_file_path)

        # get robot data
        robot = pd.json_normalize(df["current_robot_x_y_z"])

        # each row of x and y is a list; explode the values in the lists to separate rows
        df = df.explode(["date", "master_stream", "mic_in", "rnd_poetry", "flow2core", "core2flow",
                         "audio2core", "audio2flow", "flow2audio", "eda2flow",
                         "design decision", "interrupt"], ignore_index=True)

        # get date and time
        df["date"] = pd.to_datetime(df["date"])
        date = df["date"]

        # make master plot
        fig, ax = plt.subplots(6, figsize=self.figsize_xy)

        # plot audio
        ax[0].plot(date, df["mic_in"], label="mic in")
        ax[0].set_title("Human Audio")
        ax[0].set_ylabel("Amplitude")
        ax[0].set_xlabel("Time")

        # plot AI factory
        ax[1].set_title("AI Factory")
        ax[1].set_ylabel("Amplitude")
        ax[1].set_xlabel("Time")
        # ax[1].plot(date, df["rnd_poetry"])
        ax[1].plot(date, df["flow2core"], label="flow2core")
        ax[1].plot(date, df["core2flow"], label="core2flow")
        ax[1].plot(date, df["audio2core"], label="audio2core")
        ax[1].plot(date, df["audio2flow"], label="audio2flow")
        ax[1].plot(date, df["flow2audio"], label="flow2audio")
        ax[1].plot(date, df["eda2flow"], label="eda2flow")
        ax[1].legend(shadow=True, fancybox=True)

        # plot AI gesture manager/ focus
        ax[2].set_title("Gesture Manager/Focus")
        ax[2].set_ylabel("Attention Focus")
        ax[2].set_xlabel("Time")
        ax[2].plot(date, df["master_stream"])

        # plot Interrupt
        ax[3].set_title("Interrupt")
        ax[3].set_ylabel("True/ False")
        ax[3].set_xlabel("Time")
        ax[3].plot(date, df["interrupt"])

        # plot robot xyz
        ax[4].set_title("Robot xyz")
        ax[4].set_ylabel("Amplitude")
        ax[4].set_xlabel("Time")
        ax[4].plot(date, robot["x"], label="x")
        ax[4].plot(date, robot["y"], label="y")
        ax[4].plot(date, robot["z"], label="z")
        ax[4].legend(shadow=True, fancybox=True)

        # plot design decisions
        ax[5].set_title("Design Decisions")
        ax[5].set_ylabel("Movement")
        ax[5].set_xlabel("Time")
        ax[5].plot(date, df["interrupt"])

        plt.show()
        plt.savefig(self.ai_robot__images_path)

if __name__ == "__main__":
    test = AI_visualiser(path='../data/2024_11_05_1233.json')
