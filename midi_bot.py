import midi
import os
from pygame import mixer
from markov_chain import SimpleMarkovChain
from random import randint

C = 0
CS = 1
D = 2
DS = 3
E = 4
F = 5
FS = 6
G = 7
GS = 8
A = 9
AS = 10
B = 11

CMAJ = [C, D, E, F, G, A, B]
EMAJ = [E, FS, GS, A, B, CS, DS]
FMAJ = [F, G, A, AS, C, D, E]
DMIN = [D, E, F, G, A, AS, C]
DEFAULT_KEY = [C, CS, D, DS, E, F, FS, G, GS, A, AS, B]

beat = []

def playFile(file_name):
    mixer.music.load(file_name)
    mixer.music.play()
    input("Press \"enter\" to stop...")
    mixer.music.stop()

def loadRecipe(file_name, chain_notes, chain_lengths=None):
    notes = []
    pattern = midi.read_midifile(file_name)
    track1 = pattern[1]

    for i in range(len(track1)):
       # print (track1[i])
        if isinstance(track1[i], midi.events.NoteOnEvent):#("midi.NoteOnEvent" in str(note)):
            #print (track1[i])
            notes.append(track1[i])

    for i in range(len(notes)-1):
        if (notes[i].get_velocity() != 0): 
            note = notes[i]
            next_note = findNextNoteOn(notes, i)
            if (note != None and next_note != None):
                chain_notes.addChainEvent(note.get_pitch(), next_note.get_pitch())
        note_length = notes[i].tick
        next_note_length = notes[i+1].tick
        if (chain_lengths is not None):
            chain_lengths.addChainEvent(note_length, next_note_length)

def findNextNoteOn(notes, start):
    for i in range(start+1, len(notes)):
        if (i >= len(notes)):
            return 0
        if (notes[i].get_velocity() != 0):
            return notes[i]
        
##def findNoteOff(notes, start):
##    pass

##    for i in range(len(notes)-2):
##
##        if (notes[i].get_velocity() == 0):
##            chain_lengths.addChainEvent(notes[i].tick, notes[i+2].tick)
##            #print ("Pitch: {}, Next Pitch: {}".format(pitch, next_pitch))
##        else:
##            chain_notes.addChainEvent(notes[i].get_pitch(), notes[i+2].get_pitch())

def extractBeat(file_name):
    pattern = midi.read_midifile(file_name)
    track1 = pattern[0]

    beat = []

    for i in range(len(track1)-1):
        if (isinstance(track1[i], midi.events.NoteOnEvent)):
            note = track1[i].get_pitch()
            note_off = i+1
            ticks = 0
            while (note_off < len(track1) and track1[note_off].get_pitch() != note):
                ticks += track1[note_off].tick
                note_off += 1
            ticks += track1[note_off].tick
            beat.append((track1[i].tick, ticks))
    return beat
            

        

def generateNewSong(chain_notes, chain_lengths, track, beat, key=DEFAULT_KEY):
    
  #  track.append(midi.TrackNameEvent(tick=0, text='Piano right', data=[80, 105, 97, 110, 111, 32, 114, 105, 103, 104, 116]))
    track.append(midi.ProgramChangeEvent(tick=0, channel=0, data=[1]))

    first_note = chain_notes.getRandomEvent()
    while (not noteInKey(key, first_note)):
        first_note = chain_notes.getRandomEvent()

    first_length = beat[0]#chain_lengths.getRandomEvent()

    on = midi.NoteOnEvent(tick = first_length[0], velocity = 100, pitch = first_note)
    off = midi.NoteOnEvent(tick = first_length[1], velocity = 0, pitch = first_note)
    track.append(on)
    track.append(off)

    last_pitch = first_note
    #last_length = first_length

    for i in range(1, len(beat)):
        next_pitch = chain_notes.getNextEvent(last_pitch)
        while (not noteInKey(key, next_pitch)):
            next_pitch = chain_notes.getNextEvent(last_pitch)
        next_length = beat[i]
        on = midi.NoteOnEvent(tick = next_length[0], velocity = 100, pitch = next_pitch)
        off = midi.NoteOnEvent(tick = next_length[1], velocity = 0, pitch = next_pitch)
        track.append(on)
        track.append(off)

        last_pitch = next_pitch

##    for _ in range(song_length - 1):
##        next_pitch = chain_notes.getNextEvent(last_pitch)
##        while (not noteInKey(key, next_pitch)):
##            next_pitch = chain_notes.getNextEvent(last_pitch)
##        next_length = chain_lengths.getNextEvent(last_length)
##        on = midi.NoteOnEvent(tick = 0, velocity = 100, pitch = next_pitch)
##        off = midi.NoteOnEvent(tick = next_length, velocity = 0, pitch = next_pitch)
##        track.append(on)
##        track.append(off)
##
##        last_pitch = next_pitch
##        last_length = next_length

    #print (pattern)
    track.append(midi.EndOfTrackEvent(tick=1))

def noteInKey(key, note):
    root_note = note % 12 # There are 12 notes, so every note will be 0-11 when modded by 12, with C = 0
    return root_note in key

if __name__=="__main__":
    mixer.init()

    # Recipe to use as beat
    recipe_beat = os.getcwd() + "\\MidiBeats\\beat1.mid"

    recipe1 = os.getcwd() + "\\MidiFiles\\Classical\\elise.mid"

    # Sonata 8 CMAJ
    recipe2 = os.getcwd() + "\\MidiFiles\\Classical\\pathet1.mid"
    recipe3 = os.getcwd() + "\\MidiFiles\\Classical\\pathet2.mid"
    recipe4 = os.getcwd() + "\\MidiFiles\\Classical\\pathet3.mid"


    # Sonata 14 CMIN
    recipe5 = os.getcwd() + "\\MidiFiles\\Classical\\beet27m1.mid"
    recipe6 = os.getcwd() + "\\MidiFiles\\Classical\\beet27m2.mid"
    recipe7 = os.getcwd() + "\\MidiFiles\\Classical\\beet27m3.mid"

    result = os.getcwd() + "\\MidiOutput\\" + "Song1EMAJ2.mid"

    chain_notes = SimpleMarkovChain()
    chain_lengths = SimpleMarkovChain()

    recipe_list = [recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7]

    for recipe in recipe_list:
        loadRecipe(recipe, chain_notes, chain_lengths)

    #chain_notes.printChain()
    result_pattern = midi.Pattern()
    result_track = midi.Track()
    result_pattern.append(result_track)

    pattern_beat = midi.read_midifile(recipe_beat)
    for i in range(3):
        result_track.append(pattern_beat[0][i])

    beat = extractBeat(recipe_beat)
    generateNewSong(chain_notes, chain_lengths, result_track, beat, EMAJ)
    midi.write_midifile(result, result_pattern)

    for event in result_track:
        print (event)

    playFile(result)
