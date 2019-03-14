import midi
import os
from pygame import mixer

midi_file_prefix = os.getcwd() + "\\MidiFiles\\"

mixer.init()

pattern = midi.Pattern()

track = midi.Track()
pattern.append(track)

on = midi.NoteOnEvent(tick=0, velocity = 100, pitch=midi.G_3)
track.append(on)
off = midi.NoteOffEvent(tick=100, pitch=midi.G_3)
track.append(off)

on = midi.NoteOnEvent(tick=150, velocity = 100, pitch=midi.C_3)
track.append(on)
off = midi.NoteOffEvent(tick=250, pitch=midi.C_3)
track.append(off)

on = midi.NoteOnEvent(tick=300, velocity = 100, pitch=midi.A_3)
track.append(on)
off = midi.NoteOffEvent(tick=350, pitch=midi.A_3)
track.append(off)


eot = midi.EndOfTrackEvent(tick=1)


track.append(eot)

print (pattern)

midi.write_midifile("example5.mid", pattern)


#mixer.music.load(midi_file_prefix + "BlackEyedPeas\\PumpIt.mid")
#mixer.music.play()

#input("Press any key to stop...")

#mixer.music.stop()

