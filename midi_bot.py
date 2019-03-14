import midi
import os
from pygame import mixer
from markov_chain import SimpleMarkovChain
from random import randint

#
scale = []

current_note = 0
note_lengths = [60, 60, 60, 120, 60, 60, 60, 240, 60, 60, 60, 120, 60, 120, 120, 60]

def playFile(file_name):
    mixer.music.load(file_name)
    mixer.music.play()
    input("Press \"enter\" to stop...")
    mixer.music.stop()

def loadRecipe(chain, file_name):
    notes = []
    pattern = midi.read_midifile(file_name)
    track1 = pattern[1]

    for i in range(len(track1)):
        if isinstance(track1[i], midi.events.NoteOnEvent) and track1[i].get_velocity() != 0:#("midi.NoteOnEvent" in str(note)):
            notes.append(track1[i])

    for i in range(len(notes)-1):
        note = notes[i]
        next_note = notes[i+1]
        pitch = note.get_pitch()
        next_pitch = next_note.get_pitch()
        velocity = note.get_velocity()
            #print ("Pitch: {}, Next Pitch: {}".format(pitch, next_pitch))
        chain.addChainEvent(pitch, next_pitch)

def generateNewSong(chain, file_name, song_length):
    
    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)

    first_note = chain.getRandomEvent()

    on = midi.NoteOnEvent(tick = 0, velocity = 100, pitch = first_note)
    off = midi.NoteOnEvent(tick = 120, velocity = 0, pitch = first_note)
    track.append(on)
    track.append(off)

    last_pitch = first_note

    for _ in range(song_length - 1):
        next_pitch = chain.getNextEvent(last_pitch)
        on = midi.NoteOnEvent(tick = 0, velocity = 100, pitch = next_pitch)
        off = midi.NoteOnEvent(tick = getNoteLength(), velocity = 0, pitch = next_pitch)
        track.append(on)
        track.append(off)

        last_pitch = next_pitch

    #print (pattern)
    midi.write_midifile(file_name, pattern)




def getNoteLength():
    global current_note
    note_length = note_lengths[current_note]
    
    current_note += 1

    if (current_note >= len(note_lengths)):
        current_note = 0

    return note_length * 2
    #return 120#60 * randint(1, 2) * 2

if __name__=="__main__":
    mixer.init()

    recipe1 = os.getcwd() + "\\MidiFiles\\Beethoven\\elise.mid"
    recipe2 = os.getcwd() + "\\MidiFiles\\Beethoven\\opus10.mid"
    recipe3 = os.getcwd() + "\\MidiFiles\\Beethoven\\rondo.mid"
    recipe_linkin1 = os.getcwd() + "\\MidiFiles\\LinkinPark\\BurnItDown.mid"
    recipe_linkin2 = os.getcwd() + "\\MidiFiles\\LinkinPark\\Crawling.mid"
    recipe_linkin3 = os.getcwd() + "\\MidiFiles\\LinkinPark\\WhatIveDone.mid"

    
    result = os.getcwd() + "Song1_Elise.mid"

    chain = SimpleMarkovChain()

    loadRecipe(chain, recipe1)
    #loadRecipe(chain, recipe2)
    #loadRecipe(chain, recipe3)


    #chain.printChain()

    generateNewSong(chain, result, 200)

    playFile(result)
