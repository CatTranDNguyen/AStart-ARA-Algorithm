# AStart-ARA-Algorithm
use A* and ARA algorithm to find shortest path

main_ARA.py and main_AStar.py
use cmd to compile 
python main_ARA.py < input file> < output file>
if you dont pass any args, the program will open in GUI mode.

sample input file
7 # width of the matrix
0 0 # start point
6 5 # end point
0 0 0 0 0 0 0
1 0 1 1 1 0 0
1 0 1 1 1 0 0
0 0 1 0 0 0 0
0 1 1 0 1 0 0
0 0 0 0 1 0 0
1 1 1 1 1 0 0

if matrix[i][j] == 1, There is a barrier at [i][j], you can not cross that point.

sameple output file
11 #length of the path include start point and end point
(0,0) (1,1) (0,2) (0,3) (0,4) (1,5) (2,6) (3,6) (4,5) (5,6) (6,5) # path
S - x x x - -
o x o o o x -
o - o o o - x
- - o - - - x
- o o - o x -
- - - - o - x
o o o o o G -

S : start point
G : goal point
o : barrier
x : path


