# Annotation files
These two annotation files contain information about the scores of the **Jingju Music Scores Dataset** created for this repository. The files are simplified versions of those accompanying the original [**Jingju Music Scores Collection**](https://doi.org/10.5281/zenodo.1285612), in order to fit the educational purposes of this repository.

The information contained in each of the files is as follows.

#### `score-annotations.csv`

This file contains general information and metadata for each of the 33 scores of the dataset. The content of each column is the following:

0. name of the score file
1. title of the aria transcribed in the score in original Chinese script, including play and the character who sings it
2. the role type that performs the aria (either *dan* or *laosheng*)
3. the *shengqiang* (melodic framework) in which the aria is arranged (either *xipi* or *erhuang*)
4. the *banshi* (metrical pattern) in which the aria is arranged. The dataset is created to represent *manban*, *yuanban* and *kuaiban*. If more than one *banshi* is used in one aria, they are separated by semicolon. In some cases, a particular aria might contain other *banshi* besides at least one of these three main ones.
5. printed source from which the machine readable score was edited
6. [MusicBrainz](https://musicbrainz.org/) IDs for recordings of the same aria transcribed in the score. If more than one, separated by semicolon. To see the information of a particular recording in MusicBrainz, add the particular ID at the end of this URL: `https://musicbrainz.org/recording/`

#### `line-annotations.csv`

Since the melodic unit in jingju is the lyrics line, this file contains manual annotations for each lyrics line from all the scores of the dataset. The content of each column is the following:

0. name of the score file
1. role type: either *dan* or *laosheng*
2. *shengqiang* (melodic framework): either *xipi* or *erhuang*)
3. *banshi* (metrical pattern): the dataset is created to represent *manban*, *yuanban* and *kuaiban*, however some lines from particular arias might be arranged in other *banshi*.
4. line type: either opening `o` or closing `c`. In the case of *erhuang* there are two types of opening lines, `o1` for the extended one, and `o2` for the compressed one.
5. lyrics of the line (in Chinese script)
6. starting offset of the line in the corresponding score (to be used in music21)
7. ending offset of the line in the corresponding score (to be used in music21)

## License
These files are licensed under the terms of the GNU General Public License (v3).
