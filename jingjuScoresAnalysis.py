# -*- coding: utf-8 -*-

"""
The following code performs simple statistical analyses of pitch and intervals
in a dataset of jingju machine readable scores.

This script is part of the materials for the course "Computational Methods in
Ethnomusicology (Kunstuniversität Graz, 2020)"

Author: Rafael Caro Repetto (rafael.caro-repetto@kug.ac.at)

This code is licensed under the terms of the GNU General Public License (v3).
You should have received a copy of the license along with this script.  If not,
see <http://www.gnu.org/licenses/>
"""



from music21 import *
import helperFunctions as hf # Should be in the same folder
import os



################################################################################
# PITCH ANALYSIS                                                               #
################################################################################

def pitchHistogram(path2annotations, path2scoresFolder,
                   roletype=['dan', 'laosheng'],
                   shengqiang=['erhuang', 'xipi'],
                   banshi=['manban', 'yuanban', 'kuaiban'],
                   linetype=['o1', 'o2', 'o', 'c'],
                   gracenotes=True,
                   duration=True,
                   percentage=True,
                   makePlot=False):
    '''
    Prints the aggregated occurrence of each of the pitch with octave present
    in all the lyrics lines of the Jingju Music Scores Dataset that match the
    given musical features. If so selected, it plots a bar chart with the results.
    If for a particular musical feature no specific items are given, all the
    different options are selected by default. Therefore, if no musical feature
    is given at all, the analysis is performed on all the lines of the dataset.

    Args:
        path2annotations (str): path to the line-annotations.csv file,
            including the title of the file
        path2scoresFolder (str): path to the folder that contains the Jingju
            Music Scores Dataset
        roletype (list): list of strings with the selected role types, either
            'dan' or 'laosheng'
        shengqiang (list): list of strings with the selected shengqiang, either
            'erhuang' or 'xipi'
        banshi (list): list of strings with the selected banshi, either
            'manban', 'yuanban' or 'kuaiban'
        linetype (list): list of strings with the selected line type:
            'o1' for the extended opening line in erhuang
            'o2' for the compressed opening line in erhuang
            'o' for opening line in xipi
            'c' for closing line in both erhuang and xipi
        gracenotes (bool): if True, grace notes are counted in the analysis. If
            False, grace notes are ignored
        duration (bool): if True, the count of pitches is computed in terms of
            quarter length duration. If False, it is computed by number of notes
        percentage (bool): if True, the count is averaged to the total. If
            False, the count is given in absolute numbers
        makePlot (bool): if True, a bar chart is plotted with the results

    >>> pitchHistogram('./annotations/line-annotations.csv', './JMSD-xml/',
    roletype=['laosheng'], banshi=['kuaiban'], gracenotes=False,
    percentage=False)
    Occurrence of pitches:
    - C#4: 2.75 quarter notes
    - E4: 12.5 quarter notes
    - F#4: 12.75 quarter notes
    - G#4: 17.0 quarter notes
    - B4: 18.0 quarter notes
    - C#5: 7.0 quarter notes
    - E5: 1.0 quarter notes

    >>> pitchHistogram('./annotations/line-annotations.csv', './JMSD-xml/',
    roletype=['dan'], linetype=['o1'], duration=False)
    Occurrence of pitches:
    - D#4: 0.03%
    - F#4: 1.13%
    - G#4: 11.03%
    - A4: 1.04%
    - A#4: 0.03%
    - B4: 22.46%
    - C#5: 26.13%
    - D#5: 13.27%
    - E5: 9.22%
    - F#5: 12.19%
    - G#5: 3.06%
    - A5: 0.03%
    - B5: 0.34%
    - C#6: 0.03%
    '''

    # Load the annotations to the variable lineAnnotations
    with open (path2annotations, 'r', encoding='utf-8') as f:
        lineAnnotations = f.readlines()

    # COUNT PITCH --------------------------------------------------------------

    # Empty dictionary to coung pitches with octave
    pitchCount = {}

    # This variables stores the name of the score currently loaded. Therefore,
    # if a line of the same score has to be analyzed, the same score won't be
    # loaded again
    currentScore = ''

    # Iterate over all the rows of the annotations
    for row in lineAnnotations:
        # Retrieve information from each row
        scoreFile = row.split(',')[0] # score to which the line belongs
        rt = row.split(',')[1]        # role type of the line
        sq = row.split(',')[2]        # shengqiang of the line
        bs = row.split(',')[3]        # banshi of the line
        lt = row.split(',')[4]        # line type of the line
        l_start = row.split(',')[5]   # starting offset of the line
        l_end = row.split(',')[6]     # ending offset of the line
        # Check if the information about the current line matches the given
        # musical features
        if (rt in roletype and sq in shengqiang and
            bs in banshi and lt in linetype):
            # Check if the line is from a score different to the one now loaded
            if scoreFile != currentScore:
                # It is from different score:
                # Update the name of the current score
                currentScore = scoreFile
                # Create the path to the new score
                fn = os.path.join(path2scoresFolder, currentScore)
                # Load the new score
                s = converter.parse(fn)
                print('Working with', currentScore)
                # Retrieve the vocal part calling the helper function
                p = hf.getVocalPart(s)
                # Retrieve all notes
                nn = p.flat.notes.stream()
                # Iterate over notes
                for n in nn:
                    # Retrieve duration
                    nd = n.quarterLength # nd for 'note duration'
                    # If gracenotes is set to False and the duration of the
                    # current note is 0 (it is a grace note), nothing is done
                    if gracenotes or nd > 0:
                        # Retrieve pitch with octave
                        np = n.nameWithOctave # np for 'note pitch'
                        # Check if the count is computed in terms of duration
                        if duration:
                            # Update the dictionary for this pitch and duration
                            pitchCount[np] = pitchCount.get(np, 0) + nd
                        else:
                            # Update the dictionary for this pitch and 1
                            pitchCount[np] = pitchCount.get(np, 0) + 1

    print('Done!')
    print('--------------------------------------------------')

    # ORDER RESULTS ------------------------------------------------------------

    # Order the pitch names in terms of pitch height, as well as their
    # corresponding values using the helper function orderPitch().
    # This function will convert the results to percentage.
    # NOTE: the function returns three lists
    sortedMidi, sortedPitch, sortedValues = hf.orderPitch(pitchCount,
                                                          normalize=percentage)

    print('Occurrence of pitches:')

    # PRINT RESULTS ------------------------------------------------------------

    # Iterate over the indexes of the sorted pitch names
    for i in range(len(sortedPitch)):
        # Retrieve pitch name and corresponding value
        p = sortedPitch[i]  # p for 'pitch'
        v = sortedValues[i] # v for 'value'
        # Check if the results should be given as percentage
        if percentage:
            print('- {}: {:.2f}%'.format(p, v))
        else:
            # Check if the count is computed in terms of duration or notes
            if duration:
                print('- {}: {} quarter notes'.format(p, v))
            else:
                print('- {}: {} notes.'.format(p, v))

    # CREATE PLOT --------------------------------------------------------------

    # Check if a plot should be created
    if makePlot:
        # Define label for the y axis:
        # Check if the count is normalized
        if percentage:
            # Check if the count is made in terms of duration or notes
            if duration:
                label_y = 'Normalized duration'
            else:
                label_y = 'Normalized count'
        else:
            # Check if the count is made in terms of duration or notes
            if duration:
                label_y = 'Duration'
            else:
                label_y = 'Count'

        # Create the plot by calling the helper function plotHistogram()
        hf.plotHistogram(sortedMidi, sortedValues, xTicks=sortedPitch,
                      xLabel='Pitch', yLabel=label_y)



################################################################################
# INTERVAL ANALYSIS                                                            #
################################################################################

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
