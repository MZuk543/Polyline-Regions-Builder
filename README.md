# CS50 Final Project - Polyline's Regions Builder

## Video Demo:  [Project Presentation](https://youtu.be/_h4qazA1uL4)

## Description:
This is my final project for CS50’s Introduction to Programming with Python, named Polyline's Regions Builder.

The idea behind it was to code in Python a part of an algorythm that I created in my PhD dissertation in 2008, which topic was: *"The method of detection and elimination of graphic conflicts arose in automatic cartographic generalization"*. The algorithm will be called grafic conflicts free cartographic generalization algorithm (GCFCG Algorithm in short) further on.

#### The thesis short summary:
The subject of the thesis was generation of graphic conflicts by shape simplifying cartographic algorithms.
The following thesis was advanced: the modified drawing recognizability criterion usage in objects buffering enables unambiguous identification and elimination of graphic conflicts, arose in digital cartographic generalization.
The thesis covered the following scope: analysis of existing solutions, defining of conflicts, conditions to be met and elements required for their identyfication, as well as developing of conflicts detection and resolving method. In requirement of the method verification a program (that is the method's implementation in C++) was created. The comparison between Chrobak's method simplification and simplification combined with graphic conflicts resolving method was made. The method accuracy analysis was performed, showing that the obtained results conform to specifications stated in polish technical instructions related to geographic maps editing.

### The Final Project's scope:
In this project I decided to focus and to stop on two things:
- to prepare data structures and classes needed to store and process spatial data,
- to implement a method that divides a polyline into parts called regions needed in further graphical conflicts free simplification process.

#### About polyline's regions:
To be simplified according to GCFCG Algorithm a polyline needs to be divided into regions that will be divided into starshaped parts later on. Regions are here defined as fragments of the polyline that lies on one (left or right) side of a line passing through the polyline start and end point. Both regions and starshaped parts are considered essential to preserve polyline's topology in GCFCG Algorithm process.

### Input data:
The program works on a polyline consisting of vertices represented by points. Those points data are loaded from a `<data>.csv` file, stored in the project's main folder. Default file name is `data.csv`.

Two possible file's structures are assumed: with or without points' number explicitely given. In the latter case points numbers are assumed to start from 1 for the first point in the file and further on in turn.

Exemplary input file without points' numbers:
```
X,Y
173,349
210,406
191.5,486
267,558
401,531
374,470
422,414
497,349
```
Exemplary input file with points' numbers given:
```
Nr,X,Y
101,173,349
102,210,406
103,191.5,486
104,267,558
105,401,531
106,374,470
107,422,414
108,497,349
```

### Output data:
If building polyline's regions succeedes then the program writes points representing each region into a separate `.csv` files in the project's main folder. Those files names consists of the input file name followed by `_reg<NR>`, where `<NR>` is a number representing the order in which regions are being stored starting with 1 (eventually preceded with zeros - see the 599 line in `project.py`).

Exemplary output file name for the default input file name: `data_reg1.csv`

The output files' structure is the same as the input file's.

### How to execute the program:
In the terminal prompt go to the project folder and run:

```python project.py -f <data>.csv```

where `<data>` is your input file name. If no switch or input file name is given the default `data.csv` is tried.

### The Project's file structure:

    project
       ├── dcll.py
       ├── project.py
       ├── README.md
       ├── requirements.txt
       ├── test_dcll.py
       └── test_project.py

- `dcll.py` - implementation of doubly circular linked list, according to [askpython.com](https://www.askpython.com/python/examples/doubly-circular-linked-list) and to requirements of GCFCG Algorithm,
- `project.py` - implementation of spatial data classes and Polyline's Region Builder's functions,
- `README.md` - project description file,
- `requirements.txt` - list of `pip`-installable libraries that the project requires, currently empty,
- `test_dcll.py` - unitests of several methods of DCLL Class in pytest,
- `test_project.py` - unitests of functions of Polyline's Regions Builder.

### Python's libraries required:
- argparse
- csv
- collections
- os
- sys

### Other aditional libraries required:
None up till now. I decided to self implement as much as possible (and reasonable).

### Main data structures used:
- `deque` from Python's collections module - to store points or other data in cases where their order and finding neighbours matter.
- `Doubly Circular Linked List` - implemented in `dcll.py` file - to store data in a queue in cases where not only checking neighbours but also quick switching from queue's head to tail is necessary.

### Implemented classes representing spatial data:
- `Point`
- `StarshapedNode`
- `StarshapedList`
- `RegionNode`
- `RegionList`
- `Polyline`

I decided to implement my own classes representing spatial data, required by GCFCG Algorithm, back in 2008, when I implemented it for the first time. I do realise that there are lots of spatial libraries in Python, like NumPy f.e., that I could use. But I implemented my own spatial data classes again for two main reasons:
1. To stick as much as possible to my original C++ implementation.
2. For the training in Object Oriented Programming.

### Possible improvements and furter TODOs:
- to implement classes representing vertices and edges of polyline, needed to further calculation of:
- the remaining part of the graphical conflicts free cartographic generalization algorithm, containing some classic computational geometry problems.


