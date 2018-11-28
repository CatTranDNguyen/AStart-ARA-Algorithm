from tkinter import *
from tkinter import filedialog

import  os


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AIStupidDrawForm:
    __colorBlock = "orange"
    __colorStart = "dodger blue"
    __colorReset = "gray81"
    __colorGoal = "coral1"
    __colorButton = "SlateGray4"
    __colorBackground = "gray18"
    __colorGrid = "lightgray"

    __colorOn = "papaya whip" # expanded cell
    __colorChoose = "SlateGray2"
    __colorWay = "medium sea green"
    __colorSubOptimal = "PaleVioletRed1"
    __colorINCON = "SkyBlue2"
    # __colorINCON = "SlateGray2"

    __start = Point(-1, -1)
    __goal = Point(-1, -1)

    __SubOptimalWay = []
    __INCON = []

    def __UpdateCoordinateLabel(self):
        sStart = "Start (" + str(self.__start.x) + ", " + str(self.__start.y) + ")"
        sGoadl = "Goal (" + str(self.__goal.x) + ", " + str(self.__goal.y) + ")"
        self.__labelStart.config(text=sStart)
        # print(self.__labelStart.winfo_id())
        self.__labelEnd.config(text=sGoadl)
        self.__labelStart.update()
        self.__labelEnd.update()


    # DRAW ---------------------------------------------------

    def __TurnOnCell(self, row, col, color):
        x0 = col * self.__xn
        y0 = row * self.__ym
        x1 = (col + 1) * self.__xn - 1
        y1 = (row + 1) * self.__ym - 1
        return self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')

    def __DrawGlid(self):
        for i in range(self.__n):
            self.canvas.create_line(self.__xn*i - 1 , 0, self.__xn*i - 1, self.__BR.y ,fill=self.__colorGrid)
            self.canvas.create_line(0, self.__ym*i - 1, self.__BR.x, self.__ym*i - 1, fill=self.__colorGrid)

    def __DrawBlock(self, event, Click = True):
        K = Point(event.x, event.y)
        # tim rowK colK
        colK = (K.x - self.__TL.x) // self.__xn
        rowK = (K.y - self.__TL.y) // self.__ym
        # bat o rowK colK
        if (colK >= self.__n) | (rowK >= self.__n):
            return
        if self.__start is not None:
            if (rowK == self.__start.x) & (colK == self.__start.y):
                return
        if self.__goal is not None:
            if (rowK == self.__goal.x) & (colK == self.__goal.y):
                return
        # xoa neu keo
        if Click:
            if self.__block[rowK][colK] == 1:
                self.__block[rowK][colK] = 0
                self.__TurnOnCell(rowK, colK, self.__colorBackground)
                return

        self.__TurnOnCell(rowK, colK, self.__colorBlock)
        self.__block[rowK][colK] = 1

    def __DrawStart(self, event):
        K = Point(event.x, event.y)
        # tim rowK colK
        colK = (K.x - self.__TL.x) // self.__xn
        rowK = (K.y - self.__TL.y) // self.__ym
        # bat o rowK colK
        if self.__block[rowK][colK] == 1:
            return
        if self.__regStart is not None:
            self.canvas.delete(self.__regStart)
        self.__regStart = self.__TurnOnCell(rowK, colK, self.__colorStart)
        self.__start.x = rowK
        self.__start.y = colK
        self.__UpdateCoordinateLabel()

    def __DrawGoal(self, event):
        K = Point(event.x, event.y)
        # tim rowK colK
        colK = (K.x - self.__TL.x) // self.__xn
        rowK = (K.y - self.__TL.y) // self.__ym
        # bat o rowK colK
        if self.__block[rowK][colK] == 1:
            return
        if self.__regGoal is not None:
            self.canvas.delete(self.__regGoal)
        self.__regGoal = self.__TurnOnCell(rowK, colK, self.__colorGoal)
        self.__goal.x = rowK
        self.__goal.y = colK
        self.__UpdateCoordinateLabel()

    # EVENT ----------------------------------------------------

    def __OnClickButtonDrawBlock(self, event):
        self.__buttonDrawBlock.config(fg="white")
        self.__buttonDrawGoal.config(fg="black")
        self.__buttonDrawStart.config(fg="black")

        self.canvas.bind("<Button-1>", lambda event, arg=True: self.__DrawBlock(event,arg))
        self.canvas.bind("<B1-Motion>",lambda event, arg=False: self.__DrawBlock(event,arg))

    def __OnClickButtonDrawStart(self, event):
        self.__buttonDrawBlock.config(fg="black")
        self.__buttonDrawGoal.config(fg="black")
        self.__buttonDrawStart.config(fg="white")
        self.canvas.bind("<Button-1>", self.__DrawStart)
        self.canvas.unbind("<B1-Motion>", )

    def __OnClickButtonDrawGoal(self, event):
        self.__buttonDrawBlock.config(fg="black")
        self.__buttonDrawGoal.config(fg="white")
        self.__buttonDrawStart.config(fg="black")
        self.canvas.bind("<Button-1>", self.__DrawGoal)
        self.canvas.unbind("<B1-Motion>", )

    def readFile(self, fi, a, n, x1, y1, x2, y2):
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




    def __loadGUIFile(self, event):
        dir = cwd = os.getcwd()
        self.Master.filename = filedialog.askopenfilename(initialdir=dir, title="choose your file",
                                                          filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if (self.Master.filename == ""):
            return
        fo = open(self.Master.filename, "r")
        if fo is None:
            return
        n = x1 = y1 = x2 = y2 = 0
        a = []
        try:
            a, n, x1, y1, x2, y2 = self.readFile(fo, a, n, x1, y1, x2, y2)
        except (RuntimeError, TypeError, NameError, ValueError, IndexError):
            fo.close()
            return
        fo.close()
        self.drawMap(a,n,x1,y1,x2,y2)

    def __getMatrixAsString(self, a):
        s = ""
        for i in range(len(a)):
            for j in range(len(a[i]) - 1):
                if a[i][j] ==1:
                    s += "1"
                else:
                    s+="0"
                s += ' '
            s += str(a[i][len(a[i]) - 1])
            s += '\n'
        print(s)
        return s

    def __saveGUIFile(self, event):
        dir = cwd = os.getcwd()
        f = filedialog.asksaveasfile(initialdir="/", title="Save Input as", defaultextension=".txt",
                                     filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str(self.getSize()) + '\n'
        x0 = str((self.getStartPoint()).x)
        y0 = str((self.getStartPoint()).y)
        x1 = str((self.getGoalPoint()).x)
        y1 = str((self.getGoalPoint()).y)
        text2save += x0 + ' ' + y0 + '\n' + x1 + ' ' + y1 + '\n'

        text2save += self.__getMatrixAsString(self.getBlockArray())  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()  # `()` was missing.

    # SET UP COMPONENTS ----------------------------------------------------

    def __SetUpCanvas(self, master):
        self.canvas.delete("all")
        width = self.__n*15
        width = min(750,width)
        width = max(600, width)
        self.canvas.config(width=width, height=width, background=self.__colorBackground)
        self.canvas.grid(row=0)
        self.__TL = Point(0, 0)
        master.update()
        self.__start.x = -1
        self.__start.y = -1
        self.__goal.x = -1
        self.__goal.y = -1
        self.__UpdateCoordinateLabel()
        x = self.canvas.winfo_width()
        y = self.canvas.winfo_height()
        self.__xn = (x - self.__TL.x) // self.__n
        self.__ym = (y - self.__TL.y) // self.__n
        x = self.__xn * self.__n
        y = self.__ym * self.__n
        self.__BR = Point(x, y)
        self.__DrawGlid()
        self.canvas.config(width=x, height=y)
        self.canvas.update()
        self.__block = [[0 for i in range(self.__n)] for i in range(self.__n)]

    def __SetUpFrame(self, master):
        self.detailFrame = Frame(master, width=200, height=500)
        self.detailFrame.grid(row=0, column=1)

        self.variableHeuristic = StringVar(self.detailFrame)
        self.variableHeuristic.set("Euclid")  # default value
        self.__OptionHeuristic = OptionMenu(self.detailFrame, self.variableHeuristic, "Euclid", "Max(Dx, Dy)")
        self.__OptionHeuristic.config(width=10)
        self.__labelHeristic = Label(self.detailFrame, text="Heuristic: ")
        self.textBox = Entry(self.detailFrame, width=10)
        self.__labelN = Label(self.detailFrame, text="N: ")
        self.buttonFindWay = Button(self.detailFrame, text="FIND WAY", width=26, height=5, bg=self.__colorButton, fg="white", )
        self.__buttonDrawBlock = Button(self.detailFrame, text="Draw Block", width=26, height=3, bg=self.__colorBlock)
        self.__buttonReset = Button(self.detailFrame, text="Reset", width=26, height=1, bg=self.__colorReset)
        self.__buttonDrawStart = Button(self.detailFrame, text="Draw Start", width=26, height=3, bg=self.__colorStart)
        self.__buttonDrawGoal = Button(self.detailFrame, text="Draw Goal", width=26, height=3, bg=self.__colorGoal)
        self.buttonSaveFile = Button(self.detailFrame, text="Save Input", width=12, height=1, bg=self.__colorReset)
        self.buttonLoadFile = Button(self.detailFrame, text="Load Input", width=12, height=1, bg=self.__colorReset)

        self.__labelStart = Label(self.detailFrame, text="Start (-1, -1)")
        self.__labelEnd = Label(self.detailFrame, text="Goal (-1, -1)")
        self.__labelResult = Label(self.detailFrame, text="Result:")
        self.textBox.insert(END, str(self.__n))


        self.__buttonDrawBlock.bind("<Button-1>", self.__OnClickButtonDrawBlock)
        self.__buttonReset.bind("<Button-1>", self.__reset)
        self.__buttonDrawStart.bind("<Button-1>", self.__OnClickButtonDrawStart)
        self.__buttonDrawGoal.bind("<Button-1>", self.__OnClickButtonDrawGoal)
        self.buttonSaveFile.bind("<Button-1>", self.__saveGUIFile)
        self.buttonLoadFile.bind("<Button-1>", self.__loadGUIFile)


        self.textBox.bind('<Return>', self.__changeN)

        self.__labelHeristic.grid(row=0, pady=15, column=0, sticky=W)
        self.__OptionHeuristic.grid(row=0, column=1, sticky=W)
        # self.buttonFindWay.bind("<Button-1>", self.onClickFindWay)
        self.__labelN.grid(row=1,pady=15, column=0, sticky=W)
        self.textBox.grid(row=1,pady=15, column=1, sticky=W)
        self.__labelStart.grid(row=2, column=0, sticky=N+S+W)
        self.__labelResult.grid(row=2, column=1, sticky=N+S+W)
        self.__labelEnd.grid(row=3, pady=20, column=0, sticky=N+S+W)
        self.__buttonDrawBlock.grid(row=4, column=0, columnspan=2, sticky=N+S)
        self.__buttonDrawStart.grid(row=5, column=0, columnspan=2, sticky=N+S)
        self.__buttonDrawGoal.grid(row=6, column=0, columnspan=2, sticky=N+S)
        self.buttonFindWay.grid(row=7, column=0, pady=10, columnspan=2, sticky=N+S)
        self.__buttonReset.grid(row=8, column=0, columnspan=2,pady=5, sticky=N+S)

        self.buttonSaveFile.grid(row=9, column=0, sticky=W)
        self.buttonLoadFile.grid(row=9, column=1, sticky=E)

    # ----------------------------------------------------

    def __changeN(self,event):
        N = int(self.textBox.get())
        self.__resetN(N)

    def __reset(self,event):

        self.__start.x = -1
        self.__start.y = -1
        self.__goal.x = -1
        self.__goal.y = -1
        self.__SetUpCanvas(self.Master)
        self.__INCON=[]
        self.__SubOptimalWay=[]
        self.__UpdateCoordinateLabel()
        self.textBox.delete(0, 'end')
        self.textBox.insert(ANCHOR, str(self.__n))
        self.textBox.update()
        self.canvas.update()
        self.updateResult()


    def __resetN(self,N):
        # self.__labelStart = Label(self.detailFrame, text="Start (-1, -1)")
        # self.__labelEnd = Label(self.detailFrame, text="Goal (-1, -1)")

        # self.canvas.destroy()
        self.__n = N
        self.__SetUpCanvas(self.Master)
        self.__INCON = []
        self.__SubOptimalWay = []
        self.textBox.delete(0, 'end')
        self.textBox.insert(ANCHOR, str(self.__n))
        self.textBox.update()
        self.canvas.update()
        self.updateResult()


    # PUBLIC ================================================================================

    def __init__(self, master, n):
        list = master.grid_slaves()
        for l in list:
            l.destroy()
        self.__regStart = None
        self.__regGoal = None
        self.__n = n
        self.__SetUpFrame(master)

        self.canvas = Canvas(master, width=1200, height=1000, background=self.__colorBackground)
        self.__SetUpCanvas(master)
        self.Master = master

    def DrawChoose(self, row, col):
        tmp = self.__TurnOnCell(row, col, self.__colorChoose)
        self.canvas.update()
        # return tmp

    def DrawSubOptimalWay(self, row, col):
        self.__SubOptimalWay.append(self.__TurnOnCell(row, col, self.__colorSubOptimal))
        self.canvas.update()

    def EraseSubOptimalWay(self):
        for i in range(len(self.__SubOptimalWay)):
            self.__SubOptimalWay[i].config(fill=self.__colorChoose)
        self.canvas.update()

    def DrawWay(self, row, col):
        tmp = self.__TurnOnCell(row, col, self.__colorWay)
        self.canvas.update()
        # return tmp

    def DrawExpanded(self, row, col):
        self.__TurnOnCell(row, col, self.__colorOn)
        self.canvas.update()

    def DrawINCON(self,row,col):
        self.__INCON.append(self.__TurnOnCell(row, col, self.__colorINCON))
        self.canvas.update()

    def INCONToOPEN(self):
        for i in range(len(self.__SubOptimalWay)):
            self.canvas.itemconfig(self.__SubOptimalWay[i],fill=self.__colorChoose)
        for i in range(len(self.__INCON)):
            self.canvas.itemconfig(self.__INCON[i],fill=self.__colorOn)
        self.__INCON = []

    def DrawOPEN(self,row,col):
        self.DrawExpanded(row, col)

    def DrawCLOSE(self,row,col):
        self.DrawChoose(row, col)

    def getBlockArray(self):
        return self.__block

    def getStartPoint(self):
        return self.__start

    def getGoalPoint(self):
        return self.__goal

    def getSize(self):
        return self.__n

    def updateResult(self, res = None):
        s = "Result: "
        if res is not None:
             s += str(res)
        self.__labelResult.config(text=s)
        self.__labelResult.update()
    def drawMap(self,a,n,x1,y1,x2,y2):
        self.__n = n
        self.__resetN(n)
        self.__start.x = x1
        self.__start.y = y1
        self.__goal.x = x2
        self.__goal.y = y2
        if (n > x1 >= 0) & (n > y1 >= 0) & (n > x2 >= 0) & (n > y2 >= 0) & (a[x1][y1] == 0) & (a[x2][y2] == 0):
            self.__UpdateCoordinateLabel()
        else:
            print("Invalid coordinate of Start point or Goal point")
            return

        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] == 1:
                    self.__TurnOnCell(i, j, self.__colorBlock)
                    self.__block[i][j] = 1
        self.__regStart = self.__TurnOnCell(x1, y1, self.__colorStart)
        self.__regGoal = self.__TurnOnCell(x2, y2, self.__colorGoal)
        self.updateResult()
