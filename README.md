# CMiE2020-JingjuScoresAnalysis
This repository contains simple code for the analysis of a collection of machine readable scores of jingju. It is part of the materials for the course "Computational methods for ethnomusicology" (Kunstuniversität Graz, 2020). The code allows to analyze the pitch and interval structure of jingju arias by computing simple statistics and plotting histograms. Using the accompanying annotations, the analysis can be applyed to those melodic lines that belong to the selected musical features.

## Content
The repository contains two scripts. The file `jingjuScoresAnalysis.py` contains the two main functions for analysing pitch and intervals. The file `helperFunctions.py` contains a series of auxiliary functions requiered for running the first file.

The code is written using `Python 3`. It also requires the libraries [`music21`](https://web.mit.edu/music21/) and [`Matplotlib`](https://matplotlib.org/). The specific versions used for this code can be obtained from the `requirements.txt` file.

The `annotations` folder contains two files with manual annotations for the collection of machine readable scores gathered for this repository. The `line-annotations.csv` contains information for each melodic line in the collection. The `score-annotations.csv` file contains metadata and musical descriptions of each score in the collection. Please see the `README` file in that folder for more details.

## Dataset
To run the code you need the **Jingju Music Scores Dataset** specifically created for this repository. This dataset is a subset of the [**Jingju Music Scores Collection**](https://doi.org/10.5281/zenodo.1285612) developed by the [**CompMusic** project](http://compmusic.upf.edu/) from the Music Technology Group, Universitat Pompeu Fabra, Barcelona. The dataset contains 33 machine readble scores, edited using [MuseScore](https://musescore.org/) from printed sources. The dataset is designed for the study of the different elements of the jingju musical system. Therefore, it covers:

- its two main role types, namely *dan* (female characters) and *laosheng* (male characters),
- its two main *shengqiang* or melodic frameworks, namely *xipi* and *erhuang*, and
- the three more representative *banshi*, or metrical patterns, namely *manban*, *yuanban* and *kuaiban*

Due to copyright issues, the dataset is only available for research purposes under request. If you are interested, please contact [Rafael Caro](mailto:rafael.caro-repetto@kug.ac.at).

## Use
To run the code you need to install the libraries `music21` and `Matplotlib`. To simplify this task, and install the same versions used in this repository, you can use the `requirements.txt` file, by running the following command:

```
pip install -r requirements.txt
```
  
Then you should import `jingjuScoresAnalysis` to your code. For that, it is recommended to write your code in the same folder where the file `jingjuScoresAnalysis.py` is saved. It is suggested to import it in the following way:

```python
import jingjuScoresAnalysis as jsa
```
  
For the use of the two functions of this code, please refer to their docstrings.

## License
The content of this repository is licensed under the terms of the GNU General Public License (v3).
