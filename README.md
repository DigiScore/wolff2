# Wolff1

Musicking robot interacting in real-time with a musician ensemble through drawing digital score, 
designed to enhance creativity using audio captured by a microphone and physiological 
measures ([EEG](https://en.wikipedia.org/wiki/Electroencephalography) and [EDA](https://en.wikipedia.org/wiki/Electrodermal_activity)). Currently supports [Dobot Magician Lite](https://www.dobot-robots.com/products/education/magician-lite.html) and [UFactory xArm](https://www.ufactory.cc/xarm-collaborative-robot), 
uses a [BrainBit](https://brainbit.com/) EEG and [BITalino](https://www.pluxbiosignals.com/collections/bitalino) EDA. Tested on Windows 10 primarily.


## Setup a) VENV
- Install [Python 3.10](https://www.python.org/) or higher
- Install the requirements:
```bash
pip install -r requirements.txt
```
## Setup b) poetry
- Navigate inside wolff1 folder
  -     poetry shell
  -     poetry install

## Quick Start
- Connect the robot to the computer (follow XArm instructions for static IP)
- Connect the BITalino to the computer via bluetooth (passcode 1234)
- Run Open Signals [LINK](https://support.pluxbiosignals.com/knowledge-base/introducing-opensignals-revolution/)
- Run clock.py in terminal
- Record Open Signals
- Run `main.py`

## Important operational fields in config.py
- xarm_connected: bool: Is the XArm connected?
- data_logging: bool: Are you logging the robot movements?
- duration_of_piece: int: in seconds
- mic_sensitivity: int: how sensitive the live microphone
- mic_in_logging: bool: see mic input level in console
- mac_address: str: the 6 pair code for Bitalino
