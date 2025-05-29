import mido

from mido import MidiFile, Message, MidiTrack

midsource = MidiFile("cfgc_124_reaper_type1_multitrack_960ppqn_embedTEMPO.mid")

print("MIDI Type:", midsource.type)

midfinal = MidiFile()

trackfinal = MidiTrack()

midfinal.tracks.append(trackfinal)

notes = []

for msg in midsource:
    print(msg)

notes.append(msg)

#
#
# /Users/craigvear/PycharmProjects/RAMI/venv/bin/python /Users/craigvear/PycharmProjects/RAMI/tests/ignore.py
# MIDI Type: 1
# MetaMessage('track_name', name='Clipping', time=0)
# MetaMessage('smpte_offset', frame_rate=30, hours=1, minutes=0, seconds=0, frames=0, sub_frames=0, time=0)
# MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)
# MetaMessage('set_tempo', tempo=500000, time=0)
# MetaMessage('track_name', name='Track 1', time=0)
