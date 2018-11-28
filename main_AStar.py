from tkinter import *
from tkinter import filedialog

import heapq
import math
import GUI
import os
import time
import sys

OUTPUT_TXT = "AutoOutputGUI_A.txt"
N = 30

def heuristic(x, y, x1, y1, useEuclid = True):
    if useEuclid:
        return math.sqrt((x1 - x) * (x1 - x) + (y1 - y) * (y1 - y))
    else:
        return max(math.fabs(x1 - x), math.fabs(y1 - y))

class Point:
    def __init__(self, x=0, y=0, dad=None, goal=None, usEuclid = True):
        self.x = x
        self.y = y
        self.dad = dad
        self.useEuclid = usEuclid

        if dad is None:
            self.g = 1.0
        else:
            self.g = dad.g + 1
            self.useEuclid = dad.useEuclid

        if goal is None:
            self.h = 0.0
        else:
            self.h = heuristic(x, y, goal.x, goal.y, self.useEuclid)

        self.f = self.g + self.h

    def Update(self, dad, goal):

        if dad is None:
            self.g = 1.0
        else:
            self.dad = dad
            self.g = dad.g + 1
            self.useEuclid = dad.useEuclid

        if goal is None:
            self.h = 0.0
        else:
            self.h = heuristic(self.x, self.y, goal.x, goal.y, self.useEuclid)
        self.f = self.g + self.h

    def isMatched(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def isNotMatched(self, other):
        return (self.x != other.x) | (self.y != other.y)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __eq__(self, other):
        return self.f == other.f

    def __ne__(self, other):
        return self.f != other.f

    def __gt__(self, other):
        return self.f > other.f

    def __ge__(self, other):
        return self.f >= other.f

    def pr(self):
        print(str(self.x) + ", " + str(self.y))

def inside(x, y, N):
    return (x >= 0) & (x < N) & (y >= 0) & (y < N)

def TradeBack(P, GUI, Start, G, f = None, a = None):
    if P.dad is not None:
        TradeBack(P.dad, GUI, Start, G, f, a)

    if (P.isNotMatched(G) & P.isNotMatched(Start)):
        if (GUI is not None):
            GUI.Master.after(5, GUI.DrawWay(P.x, P.y))
        if a is not None:
            a[P.x][P.y] = 2

    if f is not None:
        # print("(", P.x, ",", P.y, ")", end=' ', sep='')
        # if P.isMatched(G):
        #     print()  # endline
    # else:
        tmp = "("+str(P.x)+","+str(P.y)+") "
        f.write(tmp)
        if P.isMatched(G):
            f.write("\n")  # endline

def printFile(a,n,S,Start,G,filename=None):
    if filename is None:
        fo = open(OUTPUT_TXT, "w")
    else:
        fo = open(filename, "w")
    if fo is None:
        return
    fo.write(str(int(S.f))+"\n")
    # print(int(S.f))
    TradeBack(S,None,Start,G,fo,a)
    for i in range(n):
        for j in range(n):
            if (i == Start.x) & (j == Start.y):
                fo.write("S")
            else:
                if (i == G.x) & (j == G.y):
                    fo.write("G")
                else:
                    if a[i][j]==1:
                            fo.write("o")
                    else:
                            if a[i][j]==2:
                                    fo.write("x")
                            else:
                                fo.write("-")
            if j < n - 1:
                fo.write(" ")
        fo.write("\n")
    fo.close()

def printFileError(fileOutputName):
    if fileOutputName is None:
        fo = open(OUTPUT_TXT, "w")
    else:
        fo = open(fileOutputName, "w")
    fo.write("-1")
    fo.close()

def findway(a, N, xS, yS, xG, yG, GUI = None, fileOutputName=None):
    # khoi tao
    useEuClid = True
    if GUI is not None:
        if GUI.variableHeuristic.get() != "Euclid":
            useEuClid = False
    __sleepTime = 10
    G = Point(xG, yG, None, None, useEuClid)
    Start = Point(xS, yS, None, G, useEuClid)
    S = Point(xS, yS, None, G, useEuClid)

    if (not inside(xS, yS, N)) | (not inside(xG, yG, N)):
        printFileError(fileOutputName)
        return

    dx = [1, 1, 1, 0, 0, -1, -1, -1]
    dy = [1, 0, -1, 1, -1, 1, 0, -1]
    MatrixP = [[None for x in range(N)] for y in range(N)]
    MatrixP[S.x][S.y] = S
    heap = []
    heapq.heappush(heap, S)
    while (len(heap) > 0):
        S = heapq.heappop(heap)
        if (S.isNotMatched(G) & S.isNotMatched(Start)):
            if GUI is not None:
                GUI.Master.after(__sleepTime, GUI.DrawChoose(S.x, S.y))
        else:
            if (S.isMatched(G)):
                break
        for i in range(8):
            x = S.x + dx[i]
            y = S.y + dy[i]
            if inside(x, y, N):
                if (MatrixP[x][y] is None) & (a[x][y]==0):
                    tmp = Point(x, y, S, G)
                    MatrixP[tmp.x][tmp.y] = tmp
                    heapq.heappush(heap, tmp)
                    # a[x][y] = count
                    if (tmp.isNotMatched(G)):
                        if GUI is not None:
                            GUI.Master.after(__sleepTime, GUI.DrawExpanded(x, y))
                    else:
                        break
                else:
                    if (MatrixP[x][y] is not None) & (a[x][y]!=1):
                        k = (MatrixP[x][y])
                        if k.g > 1 + (S.g):
                            (MatrixP[x][y]).Update(S, G)
                            heapq.heappush(heap, MatrixP[x][y])
                            if (tmp.isNotMatched(G)):
                                if GUI is not None:
                                    GUI.Master.after(__sleepTime, GUI.DrawExpanded(x, y))
                            else:
                                break

    if S.isMatched(G):
        if GUI is not None:
            GUI.updateResult(int(S.f))
        TradeBack(S, GUI, Start, G)
        printFile(a,N,S,Start,G,fileOutputName)
    else:
        # print(-1)
        printFileError(fileOutputName)
        if GUI is not None:
            GUI.updateResult("#####")
        print("CAN NOT FIND WAY")
        return

    print("Completed")

def onClickFindWayButton(event, form):
    a = form.getBlockArray()
    n = form.getSize()
    x1 = (form.getStartPoint()).x
    y1 = (form.getStartPoint()).y
    x2 = (form.getGoalPoint()).x
    y2 = (form.getGoalPoint()).y
    form.drawMap(a, n, x1, y1, x2, y2)
    findway(a, n, x1, y1, x2, y2, form)
    # findway(form.getBlockArray(), form.getSize(), (form.getStartPoint()).x, (form.getStartPoint()).y, (form.getGoalPoint()).x, (form.getGoalPoint()).y, form)

def readFile(fi,a,n,x1,y1,x2,y2):
    # fi = open(filename, "r")
    try:
        s = fi.read()
        i = 0
        tmp = ""
        while (s[i] != '\n'):
            tmp = tmp + s[i]
            i = i + 1
        n = int(tmp)
        tmp = ""
        while (s[i] != " "):
            tmp = tmp + s[i]
            i = i + 1
        x1 = int(tmp)
        tmp = ""
        while (s[i] != '\n'):
            tmp = tmp + s[i]
            i = i + 1
        y1 = int(tmp)
        tmp = ""
        while (s[i] != " "):
            tmp = tmp + s[i]
            i = i + 1
        x2 = int(tmp)
        tmp = ""
        while (s[i] != '\n'):
            tmp = tmp + s[i]
            i = i + 1
        y2 = int(tmp)
        tmp = ""
        c = 0
        a = [[0 for x in range(n)] for y in range(n)]
        for j in range(i + 1, len(s)):
            if (s[j] != "\n") & (s[j] != " "):
                a[int(c / n)][c % n] = int(s[j])
                c = c + 1
        return a, n, x1, y1, x2, y2
    except (RuntimeError, TypeError, NameError, ValueError, IndexError):
        print("Input File is invalid")

def main2(fi, fileOutputName):
    n = x1 = y1 = x2 = y2 = 0
    a = []
    try:
        a, n, x1, y1, x2, y2 = readFile(fInput, a, n, x1, y1, x2, y2)
    except (RuntimeError, TypeError, NameError, ValueError, IndexError):
        fInput.close()
        return
    # form.drawMap(a, n, x1, y1, x2, y2)
    findway(a,n,x1,y1,x2,y2, None, fileOutputName)

useGUI = True # only show GUI if not use command with 2 args
if len(sys.argv) >= 3:
    fileInputName = sys.argv[1]
    try:
        fInput = open(fileInputName,"r")
    except FileNotFoundError:
        fInput=None
        print("Can not open input file")
        exit()
    if fInput is not None:
        useGUI = False
        main2(fInput,sys.argv[2])
    else:
        print("Can not open input file")
if useGUI:
    root = Tk()
    root.title("A* algorithm")
    root.resizable(width=False, height=False)
    form = GUI.AIStupidDrawForm(root, N)
    (form.buttonFindWay).bind("<Button-1>", lambda event, arg=form: onClickFindWayButton(event, arg))
    # start_window(root)
    root.mainloop()