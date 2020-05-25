# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:05:21 2020

@author: Rafael Caro Repetto
"""

from music21 import *
import matplotlib.pyplot as plt

def getVocalPart(music21score):
    pp = music21score.parts
    for p in pp:
        hasLyric = False
        nn = p.flat.notes.stream()
        for n in nn[:5]:
            if n.lyric:
                hasLyric=True
        if hasLyric:
            return p
        
def orderPitch(pitchDictionary, normalize=True):
    midiPitch = {}
    for currentPitch in pitchDictionary.keys():
        currentMidi = pitch.Pitch(currentPitch).midi
        midiPitch[currentMidi] = currentPitch
    
    sortedMidi = sorted(midiPitch.keys())
    
    sortedPitch = []
    for currentMidi in sortedMidi:
        currentPitch = midiPitch[currentMidi]
        sortedPitch.append(currentPitch)
        
    if normalize:
        totalValue = sum(pitchDictionary.values())
    
    sortedValues = []
    for currentPitch in sortedPitch:
        currentValue = pitchDictionary[currentPitch]
        if normalize:
            sortedValues.append(currentValue / totalValue * 100)
        else:
            sortedValues.append(currentValue)
            
    return sortedMidi, sortedPitch, sortedValues

def orderItvl(itvlDictionary, normalize=True):
    semitonesItvl = {}
    for currentItvl in itvlDictionary.keys():
        currentSemitones = interval.Interval(currentItvl).semitones
        semitonesItvl[currentSemitones] = currentItvl
    
    sortedSemitones = sorted(semitonesItvl.keys())
    
    sortedItvl = []
    for currentSemitones in sortedSemitones:
        currentItvl = semitonesItvl[currentSemitones]
        sortedItvl.append(currentItvl)
    
    if normalize:
        totalValue = sum(itvlDictionary.values())
        
    sortedValues = []
    for currentItvl in sortedItvl:
        currentValue = itvlDictionary[currentItvl]
        if normalize:
            sortedValues.append(currentValue / totalValue * 100)
        else:
            sortedValues.append(currentValue)
        
    return sortedSemitones, sortedItvl, sortedValues

def plotHistogram(xPositions, yValues, xTicks=None, xLabel=None, yLabel=None):
    plt.bar(xPositions, yValues, color='gray')
    if xTicks:
        plt.xticks(xPositions, xTicks)
    if xLabel:
        plt.xlabel(xLabel, size=15)
    if yLabel:
        plt.ylabel(yLabel, size=15)
    plt.plot()