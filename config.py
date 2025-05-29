# [EXPERIMENT MODES]
experiment_modes = [0, 1]
# 0 = normal mode (AI)
# 1 = scripted list


# [HARDWARE]
xarm_connected = True

# [DATAWRITER]
data_logging = False
path = "data"
figsize_xy = (100, 12)
samplerate = 0.01

# [PLAY PARAMS]
silence_listener = False
duration_of_piece = 180  # 240  # in sec
speed = 5  # dynamic tempo of the all processes: 1 = slow, 10 = fast
temperature = 0

# [XARM]
# xarm1_port = '192.168.1.212'
xarm1_port = "127.0.0.1"
xarm_x_extents = [-500, 500]  # cartesian coords in mm
xarm_y_extents = [-500, 500]
xarm_z_extents = [55, 1000]
xarm_irregular_shape_extents = 50
xarm_fenced = True

# [SOUND IN]
mic_sensitivity = 10000
mic_in_prediction = 0.36
mic_in_logging = False

# [BITALINO]
baudrate = 100
channels = [0, 1, 2, 3]
mac_address = "00:21:08:35:16:D4"  # "98:D3:B1:FD:3D:1F"   "00:21:08:35:17:C0" #"98:D3:B1:FD:3D:1F"  # '/dev/cu.BITalino-3F-AE' (Linux)

# [STREAMING]
stream_list = [
    "rnd_poetry",
    "flow2core",
    "core2flow",
    "audio2core",
    "audio2flow",
    "flow2audio",
    "eda2flow",
]


"""
Notes:
To check available ports, run the following code:
    from serial.tools import list_ports

    available_ports = list_ports.comports()
    print(f'available ports: {[x.device for x in available_ports]}')

May need `sudo chmod 666 /dev/ttyACM0`
"""
