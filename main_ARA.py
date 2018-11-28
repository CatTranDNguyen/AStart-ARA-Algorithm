import multiprocessing
from tkinter import *
import heapq
import math
import GUI
import time

DELTA_EPXILON = 0.5

MAX = 1000

e = 2.5
__sleeptime = 1

OUTPUT_TXT = "autoOutputGUI_ARA.txt"


def heuristic(x, y, x1, y1, useEuclid = False):
    if useEuclid:
        return math.sqrt((x1 - x) * (x1 - x) + (y1 - y) * (y1 - y))
    else:
        return max(math.fabs(x1 - x), math.fabs(y1 - y))

     # return max(math.fabs(x1 - x), math.fabs(y1 - y))


class point:
    def fvalue(self):
        global e
        return self.g + e * self.h

    def __init__(self, x=0, y=0,dad=None, goal=None, usEuclid = False):
        self.x = x
        self.y = y
        self.dad = dad
        self.goal = goal
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
        # self.f = self.g + self.h

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
        # self.f = self.g + self.h

    def __lt__(self, other):
        return self.fvalue() < other.fvalue()

    def __le__(self, other):
        return self.fvalue() <= other.fvalue()

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def __ne__(self, other):
        return (self.x != other.x) | (self.y != other.y)

    def __gt__(self, other):
        return self.fvalue() > other.fvalue()

    def __ge__(self, other):
        return self.fvalue() >= other.fvalue()

    def isMatched(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def isNotMatched(self, other):
        return (self.x != other.x) | (self.y != other.y)


def inside(x, y, N):
    return (x >= 0) & (x < N) & (y >= 0) & (y < N)


def MinInconAndOpen(INCON, OPEN):
    Min = None
    if len(INCON) > 0:
        Min = INCON[0]
        for i in range(len(INCON)):
            if Min.g + Min.h > INCON[i].g + INCON[i].h:
                Min = INCON[i]
    if Min is None:
        Min = OPEN[0].g + OPEN[0].h
    else:
        Min = Min.g + Min.h
    for i in range(len(OPEN)):
        if Min > OPEN[i].g + OPEN[i].h:
            Min = OPEN[i].g + OPEN[i].h
    return Min


def TradeBack(P, GUI, Start, G, f=None, a=None):
    if P.dad is not None:
        TradeBack(P.dad, GUI, Start, G, f, a)

    if (P.isNotMatched(G) & P.isNotMatched(Start)):
        if (GUI is not None):
            GUI.Master.after(5, GUI.DrawSubOptimalWay(P.x, P.y))
        if a is not None:
            a[P.x][P.y] = 2

    if f is not None:
        tmp = "(" + str(P.x) + "," + str(P.y) + ") "
        f.write(tmp)
        if P.isMatched(G):
            f.write("\n")  # endline
    else:
        print("Can not open output file ")


def FinalTradeBack(P, GUI, Start, G, f=None, a=None):
    global TIMEOUT
    if P.dad is not None:
        FinalTradeBack(P.dad, GUI, Start, G, f, a)

    if (P != G) & (P != Start):
        if (GUI is not None):
            GUI.Master.after(5, GUI.DrawWay(P.x, P.y))
        if a is not None:
            a[P.x][P.y] = 2

    if f is not None:
        tmp = "(" + str(P.x) + "," + str(P.y) + ") "
        f.write(tmp)
        if P.isMatched(G):
            f.write("\n")  # endline
    else:
        print("Can not open output file")

def printFileError(fo):
    if fo is not None:
        fo.write("-1")
    print("CAN NOT FIND WAY")


def printFile(a, n, S, Start, G, fo, GUI, isfinal=False):
    if fo is None:
        return
    fo.write("f = " + str(int(S.fvalue())) + "\n")
    # print("f = " + str(int(S.fvalue())))
    if isfinal:
        FinalTradeBack(S,GUI,Start,G,fo,a)
    else:
        TradeBack(S, GUI, Start, G, fo, a)
    for i in range(n):
        for j in range(n):
            if (i == Start.x) & (j == Start.y):
                fo.write("S")
            else:
                if (i == G.x) & (j == G.y):
                    fo.write("G")
                else:
                    if a[i][j] == 1:
                        fo.write("o")
                    else:
                        if a[i][j] == 2:
                            fo.write("x")
                            a[i][j] = 0
                        else:
                            fo.write("-")
            if j < n - 1:
                fo.write(" ")
        fo.write("\n")
        # if ~isfinal:
        #     fo.write("\n")

    # fo.close()

def inArrayPoint(a,x,y):
    for i in range(len(a)):
        if (a[i].x==x) & (a[i].y==y):
            return True
    return False


def addToIncon(INCONS, p):
    if p not in INCONS:
        INCONS.append(p)
    else:
        for i in range(len(INCONS)):
            if INCONS[i]==p:
                INCONS[i] = p

def improvePath(a, S, G, N, heapO, Close, INCONS, GUI, MatrixP):
    dx = [0, 0, 1, 1, 1, -1, -1, -1]
    dy = [1, -1, 1, 0, -1, 1, 0, -1]

    P = S
    MatrixP[P.x][P.y] = P
    count = 2
    # a[P.x][P.y] = -1
    while len(heapO) > 0:
        if G.fvalue() > heapO[0].fvalue():
            P = heapq.heappop(heapO)
            Close.append(P)
            if (GUI is not None) & (P != S) & (P != G):
                GUI.Master.after(__sleeptime, GUI.DrawCLOSE(P.x, P.y))
            if P != G:
                for i in range(8):
                    x = P.x + dx[i]
                    y = P.y + dy[i]
                    if inside(x, y, N):
                        if a[x][y] != 1:
                            if MatrixP[x][y] is None:
                                tmp = point(x, y, P, G)
                                tmp.g = MAX
                                MatrixP[x][y] = tmp
                            if MatrixP[x][y].g > 1 + P.g:
                                (MatrixP[x][y]).Update(P, G)
                                tmp = MatrixP[x][y]
                                if inArrayPoint(Close,x,y) == False:
                                    if MatrixP[x][y] in heapO:
                                        for i in range(len(heapO)):
                                            if MatrixP[x][y] == heapO[i]:
                                                heapO[i] = MatrixP[x][y]
                                                tmp = heapO[0]
                                                heapO[0] = heapO[i]
                                                heapO[i] = tmp
                                                heapq.heapify(heapO)
                                    else:
                                        heapq.heappush(heapO, MatrixP[x][y])
                                    if GUI is not None:
                                        if tmp != G:
                                            GUI.Master.after(__sleeptime, GUI.DrawOPEN(x, y))
                                else:
                                    addToIncon(INCONS,MatrixP[x][y])
                                    if GUI is not None:
                                        if tmp != G:
                                            GUI.Master.after(__sleeptime, GUI.DrawINCON(x, y))

            else:
                break
        else:
            break

    if P == G:
        return P
    else:
        return None


def findway(a, N, xS, yS, xG, yG, GUI=None, fileOutputName=None):

    if GUI is not None:
        if GUI.variableHeuristic.get() != "Euclid":
            useEuClid = False
    MatrixP = [[None for x in range(N)] for y in range(N)]
    G = point(xG, yG, None, None)
    Start = point(xS, yS, None, G)
    S = point(xS, yS, None, G)
    G.g = MAX

    global e
    e = 2.5
    heapOPEN = []
    CLOSE = []
    INCONS = []
    if fileOutputName is not None:
        fOutput = open(fileOutputName, "w")
    else:
        fOutput = open(OUTPUT_TXT, "w")

    if (not inside(xS, yS, N)) | (not inside(xG, yG, N)):
        # print(-1)
        printFileError(fOutput)
        if GUI is not None:
            GUI.updateResult("#####")
        return

    heapq.heappush(heapOPEN, S)
    tmp = improvePath(a, S, G, N, heapOPEN, CLOSE, INCONS, GUI, MatrixP)
    if tmp is None:  # khong tim thay duong di
        printFileError(fOutput)
        fOutput.close()
        if GUI is not None:
            GUI.updateResult("#####")
        return

    else:  # cai tien duong di
        G = P = tmp
        if fOutput is not None:
            tmp = "e = " + str(e) + '\n'
            # print(e)
            fOutput.write(tmp)
            printFile(a, N, P, Start, G, fOutput, GUI)
        tmp = MinInconAndOpen(INCONS, heapOPEN)
        Min = G.g / MinInconAndOpen(INCONS, heapOPEN)
        et = min(e, Min)

        while et > 1:
            e = e - DELTA_EPXILON
            for i in range(len(heapOPEN)):
                INCONS.append(heapq.heappop(heapOPEN))
            for i in range(len(INCONS)):
                heapq.heappush(heapOPEN, INCONS[i])
            if GUI is not None:
                GUI.INCONToOPEN()
            INCONS = []
            CLOSE = []
            tmp = improvePath(a, S, G, N, heapOPEN, CLOSE, INCONS, GUI, MatrixP)
            if tmp is not None:
                G = tmp
            Min = G.g / MinInconAndOpen(INCONS, heapOPEN)
            et = min(e, Min)
            P = G
            if fOutput is not None:
                # print(e)
                tmp = "e = " + str(e) + '\n'
                fOutput.write(tmp)
                printFile(a, N, P, Start, G, fOutput, GUI)
        P = G

        tmp = "FINAL RESULT" + '\n'
        fOutput.write(tmp)
        printFile(a, N, P, Start, G, fOutput, GUI, True)
        fOutput.close()
        if GUI is not None:
            GUI.updateResult(int(P.fvalue()))
        print("Completed")


def onClickFindWayButton(event, form):
    a = form.getBlockArray()
    n = form.getSize()
    x1 = (form.getStartPoint()).x
    y1 = (form.getStartPoint()).y
    x2 = (form.getGoalPoint()).x
    y2 = (form.getGoalPoint()).y
    form.drawMap(a,n,x1,y1,x2,y2)
    findway(a, n, x1, y1, x2, y2, form)


def readFile(fi, a, n, x1, y1, x2, y2):
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

TIMEOUT = 1
if __name__ == '__main__':
    n = x1 = y1 = x2 = y2 = 0
    a = []

    useGUI = True  # only show GUI if not use command with 2 args
    if len(sys.argv) >= 3:
        fileInputName = sys.argv[1]
        try:
            fInput = open(fileInputName, "r")
        except FileNotFoundError:
            fInput = None
            print("Can not open input file")
            exit()
        if fInput is not None:
            useGUI = False
            n = x1 = y1 = x2 = y2 = 0
            a = []
            try:
                a, n, x1, y1, x2, y2 = readFile(fInput, a, n, x1, y1, x2, y2)
            except (RuntimeError, TypeError, NameError, ValueError, IndexError):
                fInput.close()
                exit()
            if len(sys.argv) ==4:
                try:
                    TIMEOUT = float(sys.argv[3])
                except ValueError:
                    TIMEOUT = 1

            process = multiprocessing.Process(target=findway, args=(a, n, x1, y1, x2, y2, None, sys.argv[2]))
            process.start()

            process.join(TIMEOUT)
            if process.is_alive():
                # print("running... let's kill it...")
                process.terminate()
                process.join()
                print("TIME OUT!")
        else:
            print("Can not open input file")
    if useGUI:
        root = Tk()
        root.title("ARA* algorithm")
        root.resizable(width=False, height=False)
        N = 7
        form = GUI.AIStupidDrawForm(root, N)
        (form.buttonFindWay).bind("<Button-1>", lambda event, arg=form: onClickFindWayButton(event, arg))
        root.mainloop()
