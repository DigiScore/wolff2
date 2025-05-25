# Wolff2

Wolff2 is a digital score. It is a realisation of Christian Wolff’s famous composition 
_For 1, 2 or 3 Players_ (1964) conceptualized as an interactive robot. 
The robot is embedded with AI that has been trained on Wolff’s original score and will work with 
a performer in realtime to realise the music.

## Setup a) VENV
- Install [Python 3.10](https://www.python.org/) or higher
- Install the requirements:
```bash
pip install -r requirements.txt
```
## Setup b) poetry
- Navigate inside wolff2 folder
  -     poetry env activate
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

## To run the robot simulator
https://forum.ufactory.cc/t/ufactory-studio-simulation/3719
