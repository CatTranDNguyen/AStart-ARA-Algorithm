# AStart-ARA-Algorithm
use A* and ARA algorithm to find shortest path


## Installing

Use cmd to compile two file **main_AStar.py** for A* algorithm and  **main_ARA.py** for ARA algorithm.
```
python main_AStar.py  < input file > < output file> 
```
**GUI:** if you want to open in GUI mode, don't pass any args.
```
python main_AStar.py
```

### Input Output file

#### INPUT 
Line 1: integer N : NxN matrix

Line 2: 2 integers X0, Y0: Start(X0, Y0)

Line 3: 2 integers X0, Y0: Goal(X0, Y0)

Next N lines:
N symbols (0 or 1) indicating free space (0) or obstacle (1). 

```
7
0 0
6 5
0 0 0 0 0 0 0
1 0 1 1 1 0 0
1 0 1 1 1 0 0
0 0 1 0 0 0 0
0 1 1 0 1 0 0
0 0 0 0 1 0 0
1 1 1 1 1 0 0
```
#### OUTPUT

Line 1: integer L: Length of the path (including Start Point and End Point)

Line 2: Path Order

Next N lines:
N symbols indicating free space (-), obstacle (o), path (x), Start Point (S) or Goal Point (G).

```
11
(0,0) (1,1) (0,2) (0,3) (0,4) (1,5) (2,6) (3,6) (4,5) (5,6) (6,5) 
S - x x x - -
o x o o o x -
o - o o o - x
- - o - - - x
- o o - o x -
- - - - o - x
o o o o o G -
```

## Authors

* **Cat Tran D. Nguyen** - [Trân](https://github.com/HeyIamKi)
* **Huyen Tram Dang**


