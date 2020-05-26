# -*- coding: utf-8 -*-

"""
The following code contains auxiliary functions to be used in the script
jingjuScoresAnalysis.py.

This script is part of the materials for the course "Computational Methods in
Ethnomusicology (Kunstuniversität Graz, 2020)"

Author: Rafael Caro Repetto (rafael.caro-repetto@kug.ac.at)

This code is licensed under the terms of the GNU General Public License (v3).
You should have received a copy of the license along with this script.  If not,
see <http://www.gnu.org/licenses/>
"""



from music21 import *
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------

def getVocalPart(music21score):
    '''
    Returns the part of a given loaded score in music21 that contains lyrics.
    This code assumes that only one part contains lyrics.

    Args:
        music21score (music21.stream.Score): a score loaded in music21 as a
            score stream object.

    Returns:
        part (music21.stream.Part): the part from the the given score that
            contains lyrics as a part stream object
    '''

    # Retrieve parts from the score stream
    pp = music21score.parts

    # Iterate over the parts
    for p in pp:
        # Initiate a checker for lyrics as False by default
        hasLyric = False
        # Retrieve all the notes from the current part
        nn = p.flat.notes.stream()
        # Iterate over the first 5 notes
        for n in nn[:5]:
            # Check if any note has a lyric
            if n.lyric:
                # Update the lyrics checker to True
                hasLyric=True
        # After iterating over the firt 5 notes, check if there are lyrics in
        # the current part
        if hasLyric:
            # Return the current part (the function stops working)
            return p

# ------------------------------------------------------------------------------

def orderPitch(pitchDictionary, normalize=True):
    '''
    Given a dictionary with a count of pitches, it orders the pitch names in
    terms of pitch height and returns the ordered list of the midi values
    corresponding to the pitch names in the dictionary, the corresponding
    ordered list of pitch names, and the corresponding ordered list of count
    values. If so selected, the values are noramalized to the total.

    Args:
        pitchDictionary (dict): a dictionary whose keys are pitch names and
            values are count of those pitch names
        normalize (bool): if True, the values are normalized to the total. If
            False, the values are kept unchanged

    Returns:
        sortedMidi (list): a list with the ordered midi values corresponding to
            the pitch names in the dictionary
        sortedPitch (list): a list with the pitch names in the dictionary
            ordered according to their corresponding midi values
        sortedValues (list): a list with the values (normalized or not) of
            the dictionary ordered according to the midi values of their
            corresponding pitch names

    >>> orderPitch({'A4': 66, 'B4': 137, 'G#4': 422, 'F#4': 500, 'E4': 286,
    'C#4': 754, 'B3': 450, 'D#4': 280, 'C#5': 9, 'G#3': 1})
    ([56, 59, 61, 63, 64, 66, 68, 69, 71, 73],
     ['G#3', 'B3', 'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A4', 'B4', 'C#5'],
     [0.034423407917383825,
      15.49053356282272,
      25.9552495697074,
      9.63855421686747,
      9.845094664371773,
      17.21170395869191,
      14.526678141135974,
      2.2719449225473323,
      4.716006884681583,
      0.3098106712564544])

    >>> orderPitch({'F#4': 215, 'A4': 11, 'G#4': 137, 'B4': 49, 'C#5': 4,
    'C#4': 245, 'E4': 151, 'B3': 176, 'D#4': 115, 'G#3': 64, 'A3': 4, 'F#3': 4},
    normalize=False)
    ([54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73],
     ['F#3',
      'G#3',
      'A3',
      'B3',
      'C#4',
      'D#4',
      'E4',
      'F#4',
      'G#4',
      'A4',
      'B4',
      'C#5'],
     [4, 64, 4, 176, 245, 115, 151, 215, 137, 11, 49, 4])
    '''

    # Empty dictionary for retrieving midi values as keys, with their
    # corresponding pitch name as value
    midiPitch = {}
    # Iterate over the pitch names in the given dictionary, that is, its keys
    for currentPitch in pitchDictionary.keys():
        # Create a pitch object with the current pitch name and retrieve its
        # midi value
        currentMidi = pitch.Pitch(currentPitch).midi
        # Update the midiPitch dictionary with the current midi value as key,
        # and its corresponding pitch name as value
        midiPitch[currentMidi] = currentPitch

    # Order the midi values, that is, the keys of the midiPitch dictionary
    sortedMidi = sorted(midiPitch.keys())

    # Empty list to save the ordered pitch names
    sortedPitch = []
    # Iterate over the ordered midi values
    for currentMidi in sortedMidi:
        # Retrieve the pitch name corresponding to the current midi value from
        # the midiPitch dictionary
        currentPitch = midiPitch[currentMidi]
        # Append the current pitch name to the sortedPitch list
        sortedPitch.append(currentPitch)

    # Before ordering the values, check if they should be normalized
    if normalize:
        # They should be normalized: compute the total
        totalValue = sum(pitchDictionary.values())

    # Empty list to save the ordered values
    sortedValues = []
    # Iterate over the ordered pitch names
    for currentPitch in sortedPitch:
        # Retrieve the value corresponding to the current pitch name from
        # the dictionary given as parameter of the function
        currentValue = pitchDictionary[currentPitch]
        # Check if the value should be normalized
        if normalize:
            # Should be normalized: compute percentage and append it to the
            # sortedValues list
            sortedValues.append(currentValue / totalValue * 100)
        else:
            # Should NOT be normalized: append the value to the sortedValues
            # list without any change
            sortedValues.append(currentValue)

    # Return the ordered lists
    return sortedMidi, sortedPitch, sortedValues

# ------------------------------------------------------------------------------

def orderItvl(itvlDictionary, normalize=True):
    '''
    Given a dictionary with a count of intervals, it orders the interval names
    in terms of their semitones and returns the ordered list of semitones
    corresponding to the interval names in the dictionary, the corresponding
    ordered list of interval names, and the corresponding ordered list of count
    values. If so selected, the values are noramalized to the total.

    Args:
        itvlDictionary (dict): a dictionary whose keys are interval names and
            values are count of those interval names
        normalize (bool): if True, the values are normalized to the total. If
            False, the values are kept unchanged

    Returns:
        sortedSemitones (list): a list with the ordered semitones corresponding
            to the interval names in the dictionary
        sortedItvl (list): a list with the interval names in the dictionary
            ordered according to their corresponding semitones
        sortedValues (list): a list with the values (normalized or not) of
            the dictionary ordered according to the semitones of their
            corresponding interval names

    >>> orderItvl({'m3': 246, 'm2': 19, 'P4': 56, 'M2': 485, 'M3': 38, 'P5':
    26, 'P1': 143, 'm6': 8, 'M6': 1, 'm7': 7})
    ([0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
     ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'P5', 'm6', 'M6', 'm7'],
     [13.896987366375122,
      1.84645286686103,
      47.13313896987366,
      23.9067055393586,
      3.69290573372206,
      5.442176870748299,
      2.5267249757045676,
      0.7774538386783284,
      0.09718172983479105,
      0.6802721088435374])

    >>> orderItvl({'m3': 114, 'm-2': 13, 'P-4': 31, 'M2': 206, 'm2': 6, 'M-2':
    279, 'm-3': 132, 'M3': 17, 'M-3': 21, 'P5': 21, 'P4': 25, 'P1': 143, 'm-6':
    5, 'm6': 3, 'P-5': 5, 'M6': 1, 'm-7': 6, 'm7': 1}, normalize=False)
    ([-10, -8, -7, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
     ['m-7',
      'm-6',
      'P-5',
      'P-4',
      'M-3',
      'm-3',
      'M-2',
      'm-2',
      'P1',
      'm2',
      'M2',
      'm3',
      'M3',
      'P4',
      'P5',
      'm6',
      'M6',
      'm7'],
     [6, 5, 5, 31, 21, 132, 279, 13, 143, 6, 206, 114, 17, 25, 21, 3, 1, 1])
    '''

    # Empty dictionary for retrieving semitones as keys, with their
    # corresponding interval name as value
    semitonesItvl = {}
    # Iterate over the interval names in the given dictionary, that is, its keys
    for currentItvl in itvlDictionary.keys():
        # Create an interval object with the current interval name and retrieve
        # its semitones
        currentSemitones = interval.Interval(currentItvl).semitones
        # Update the semitonesItvl dictionary with the current semitones as key,
        # and its corresponding interval name as value
        semitonesItvl[currentSemitones] = currentItvl

    # Order the semitones, that is, the keys of the semitonesItvl dictionary
    sortedSemitones = sorted(semitonesItvl.keys())

    # Empty list to save the ordered interval names
    sortedItvl = []
    # Iterate over the ordered semitones
    for currentSemitones in sortedSemitones:
        # Retrieve the interval name corresponding to the current semitones from
        # the semitonesItvl dictionary
        currentItvl = semitonesItvl[currentSemitones]
        # Append the current interval name to the sortedItvl list
        sortedItvl.append(currentItvl)

    # Before ordering the values, check if they should be normalized
    if normalize:
        # They should be normalized: compute the total
        totalValue = sum(itvlDictionary.values())

    # Empty list to save the ordered values
    sortedValues = []
    # Iterate over the ordered interval names
    for currentItvl in sortedItvl:
        # Retrieve the value corresponding to the current interval name from
        # the dictionary given as parameter of the function
        currentValue = itvlDictionary[currentItvl]
        # Check if the value should be normalized
        if normalize:
            # Should be normalized: compute percentage and append it to the
            # sortedValues list
            sortedValues.append(currentValue / totalValue * 100)
        else:
            # Should NOT be normalized: append the value to the sortedValues
            # list without any change
            sortedValues.append(currentValue)

    # Return the ordered lists
    return sortedSemitones, sortedItvl, sortedValues

# ------------------------------------------------------------------------------

def plotHistogram(xPositions, yValues, xTicks=None, xLabel=None, yLabel=None):
    '''
    Plots a bar chart with the given values for the given positions. If ticks
    for the x axis are given, they are added. If labels for the x and y axes
    are given, they are added.

    Args:
        xPositions (list): a list of numbers with the positions of the bars in
            the x axis
        yValues (list): a list of numbers with height of the bars in the y axis
        xTicks (list): a list of strings with the ticks for the bars in the x
            axis
        xLabel (str): a string with the label for the x axis
        yLabel (str): a string with the label for the y axis
    '''

    # Initiate the plot
    plt.bar(xPositions, yValues, color='gray')

    # Add the ticks for the x axis, if given
    if xTicks:
        plt.xticks(xPositions, xTicks)

    # Add a label for the x axis, if given
    if xLabel:
        plt.xlabel(xLabel, size=15)

    # Add a label for the y axis, if given
    if yLabel:
        plt.ylabel(yLabel, size=15)

    # Close and display the plot
    plt.plot()
