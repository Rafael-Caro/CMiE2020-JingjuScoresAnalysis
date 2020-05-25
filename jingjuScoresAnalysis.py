# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:20:51 2020

@author: Rafael Caro Repetto
"""

from music21 import *
import helperFunctions as hf
import os        

def pitchHistogram(path2annotations, path2scoresFolder,
                   roletype=['dan', 'laosheng'],
                   shengqiang=['erhuang', 'xipi'],
                   banshi=['manban', 'yuanban', 'kuaiban'],
                   linetype=['o1', 'o2', 'o', 'c'],
                   gracenotes=True,
                   duration=True,
                   percentage=True,
                   makePlot=False):
    with open (path2annotations, 'r', encoding='utf-8') as f:
        lineAnnotations = f.readlines()
        
    pitchCount = {}
    
    currentScore = ''
    
    for row in lineAnnotations:
        scoreFile = row.split(',')[0]
        rt = row.split(',')[1] # role type
        sq = row.split(',')[2] # shengqiang
        bs = row.split(',')[3] # banshi
        lt = row.split(',')[4] # line type
        l_start = row.split(',')[5]
        l_end = row.split(',')[6]
        if (rt in roletype and sq in shengqiang and
            bs in banshi and lt in linetype):
            if scoreFile != currentScore:
                currentScore = scoreFile
                fn = os.path.join(path2scoresFolder, currentScore)
                s = converter.parse(fn)
                print('Working with', currentScore)
                p = hf.getVocalPart(s)
                nn = p.flat.notes.stream()
                for n in nn:
                    nd = n.quarterLength # note duration
                    if gracenotes or nd > 0:
                        np = n.nameWithOctave # note pitch
                        if duration:                        
                            pitchCount[np] = pitchCount.get(np, 0) + nd
                        else:
                            pitchCount[np] = pitchCount.get(np, 0) + 1
                        
    print('Done!')
    print('--------------------------------------------------')
    
    sortedMidi, sortedPitch, sortedValues = hf.orderPitch(pitchCount,
                                                          normalize=percentage)
    
    print('Occurrence of pitches:')
    
    for i in range(len(sortedPitch)):
        p = sortedPitch[i] # pitch
        v = sortedValues[i] # value
        if percentage:
            print('- {}: {:.2f}%'.format(p, v))
        else:
            if duration:
                print('- {}: {} quarter notes'.format(p, v))
            else:
                print('- {}: {} notes.'.format(p, v))
                
    if makePlot:
        if percentage:
            if duration:
                label_y = 'Normalized duration'
            else:
                label_y = 'Normalized count'
        else:
            if duration:
                label_y = 'Duration'
            else:
                label_y = 'Count'
        hf.plotHistogram(sortedMidi, sortedValues, xTicks=sortedPitch,
                      xLabel='Pitch', yLabel=label_y)
        
def intervalHistogram(path2annotations, path2scoresFolder,
                      roletype=['dan', 'laosheng'],
                      shengqiang=['erhuang', 'xipi'],
                      banshi=['manban', 'yuanban', 'kuaiban'],
                      linetype=['o1', 'o2', 'o', 'c'],
                      directed=False,
                      percentage=True,
                      makePlot=False):
    with open (path2annotations, 'r', encoding='utf-8') as f:
        lineAnnotations = f.readlines()
        
    itvlCount = {}
    
    currentScore = ''
    
    for row in lineAnnotations:
        scoreFile = row.split(',')[0]
        rt = row.split(',')[1] # role type
        sq = row.split(',')[2] # shengqiang
        bs = row.split(',')[3] # banshi
        lt = row.split(',')[4] # line type
        l_start = row.split(',')[5]
        l_end = row.split(',')[6]
        if (rt in roletype and sq in shengqiang and
            bs in banshi and lt in linetype):
            if scoreFile != currentScore:
                currentScore = scoreFile
                fn = os.path.join(path2scoresFolder, currentScore)
                s = converter.parse(fn)
                print('Processing', currentScore)
                p = hf.getVocalPart(s)
                nr = p.flat.notesAndRests.stream()
                for i in range(len(nr)-1):
                    n1 = nr[i]
                    n2 = nr[i+1]
                    if n1.isNote and n2.isNote:
                        itvl = interval.Interval(n1, n2)
                        if directed:
                            itvlName = itvl.directedName
                        else:
                            itvlName = itvl.name
                        itvlCount[itvlName] = itvlCount.get(itvlName, 0) + 1
                        
    print('Done!')
    print('--------------------------------------------------')
    
    sortedSemitones, sortedItvl, sortedValues = hf.orderItvl(itvlCount,
                                                          normalize=percentage)
    
    print('Occurrence of intervals:')
    for i in range(len(sortedItvl)):
        if percentage:
            print('- {}: {:.2f}%'.format(sortedItvl[i], sortedValues[i]))
        else:
            print('- {}: {} times'.format(sortedItvl[i], sortedValues[i]))

    if makePlot:
        if percentage:
            label_y = 'Normalized count'
        else:
            label_y = 'Count'
        hf.plotHistogram(sortedSemitones, sortedValues, sortedItvl,
                      xLabel='Interval', yLabel=label_y)