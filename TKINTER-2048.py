#********************IMPORTS******************
import tkinter as tk
import numpy as math
import time
import os
#*******************VARIABLES*****************
BLK = "Blank"
BoardMatrix = math.array([(BLK, BLK, BLK, BLK), (BLK, BLK, BLK, BLK), (BLK, BLK, BLK, BLK), (BLK, BLK, BLK, BLK)])                       
BoardXMatrix = math.array([(145, 265, 385, 505), (145, 265, 385, 505), (145, 265, 385, 505), (145, 265, 385, 505)])
BoardYMatrix = math.array([(200, 200, 200, 200), (320, 320, 320, 320), (440, 440, 440, 440), (560, 560, 560, 560)])
SpacesToMove = 0
ScoreNum = 0

#SpawnRandomTile() Variables
OpenSpaces = []
ChosenRow = 0
ChosenSpace = 0

#Tile Colors
TileColor = ["#E3D6C9","#ECD8C1","#E39C5F","#EE8C59","#F08268", "#EA4C28", "#E9D372", "#D5B44A", "#EAD04D", "#F5DE36", "#EBD024", "#F08F73", "#D54A3C", "#ED5127", "#67B6D8", "#4188A7" ]

#*******Create the Master Title, Score, and Canvas*******
#create the window as a master
master = tk.Tk()
master.title("2048")
master.maxsize(750, 800)

#create the canvas and pack it in the master
canvas = tk.Canvas(master, width=750, height=700)
canvas.pack()

#Create The Title
Title = canvas.create_text(375, 65, text="2048", font=("Helvetica","85"), anchor="e")
canvas.tag_lower("Title")

#create the Scorebox
Prompt = canvas.create_text(250, 150, text="Score:", font=("Helvetica","25"), anchor="e")
canvas.tag_raise("Prompt")
ScoreOutline = canvas.create_rectangle(265, 135, 380, 175)
Score = canvas.create_text(322, 155, text=ScoreNum, font=("Helvetica","23"))

#create quit button
tk.Button(master, text="Quit", command=master.destroy, width=750, height=50, font=("Helvetica", "50")).pack()
#*******************FUNCTIONS*****************

def SpawnTile(x, y, num):
    root = 1
    ans = int(num)
    while ans != 2:
        ans = ans/2
        root += 1
    canvas.create_rectangle(x, y, x + 100 , y + 100, fill=TileColor[root - 1], outline="", tag="tile")
    canvas.create_text(x+50, y+50, text=str(num), tag="tile", font=("Helvetica", "16"))
    
def CheckForEmpty():
    if (BLK in BoardMatrix[0] or BLK in BoardMatrix[1] or BLK in BoardMatrix[2] or BLK in BoardMatrix[3]):
        return True
    else:
        return False

    
def SpawnRandomTile():
    OpenSpaces = []
    ChosenRow = 0
    ChosenSpace = 0
    OpenSpaces = [(ChosenRow, ChosenSpace) for ChosenRow in range(4) for ChosenSpace in range(4) if BoardMatrix[ChosenRow][ChosenSpace] == BLK]
    ChosenRow, ChosenSpace = OpenSpaces[math.random.randint(0, len(OpenSpaces))]
    BoardMatrix[ChosenRow][ChosenSpace] = 2
    SpawnTile(BoardXMatrix[ChosenRow][ChosenSpace], BoardYMatrix[ChosenRow][ChosenSpace], 2)

def MoveTiles(direction):
    global BoardMatrix
    InvertedBoard = BoardMatrix.T
    if (direction == 1):          #left
        SpacesToMove = 0
        for i in range(4):
            SpacesToMove = 0
            for j in range(4):
                if (BoardMatrix[i][j] == BLK): SpacesToMove += 1
                #blank spot
                else: #something is their
                    if (SpacesToMove == 0):
                        pass
                    else:
                        BoardMatrix[i][j - SpacesToMove] = BoardMatrix[i][j]
                        BoardMatrix[i][j] = BLK
                        
    if (direction == 2):        #right
        SpacesToMove = 0
        for i in range(4):
            SpacesToMove = 0
            for j in range(3, -1, -1):
                if (BoardMatrix[i][j] == BLK): SpacesToMove += 1
                #blank spot
                else: #something is their
                    if (SpacesToMove == 0):
                        pass
                    else:
                        BoardMatrix[i][j + SpacesToMove] = BoardMatrix[i][j]
                        BoardMatrix[i][j] = BLK
                        
    if (direction == 3):          #up
        SpacesToMove = 0
        for i in range(4):
            SpacesToMove = 0
            for j in range(4):
                if (InvertedBoard[i][j] == BLK): SpacesToMove += 1
                #blank spot
                else: #something is their
                    if (SpacesToMove == 0):
                        pass
                    else:
                        InvertedBoard[i][j - SpacesToMove] = InvertedBoard[i][j]
                        InvertedBoard[i][j] = BLK
        BoardMatrix = InvertedBoard.T

    if (direction == 4):          #down
        SpacesToMove = 0
        for i in range(4):
            SpacesToMove = 0
            for j in range(3, -1, -1):
                if (InvertedBoard[i][j] == BLK): SpacesToMove += 1
                #blank spot
                else: #something is their
                    if (SpacesToMove == 0):
                        pass
                    else:
                        InvertedBoard[i][j + SpacesToMove] = InvertedBoard[i][j]
                        InvertedBoard[i][j] = BLK
        BoardMatrix = InvertedBoard.T    

def MergeTiles(direction):
    global BoardMatrix
    global ScoreNum
    InvertedBoard = BoardMatrix.T
    
    if (direction == 1): # Left
        for i in range(4):
            for j in range(3):
                if (BoardMatrix[i][j] == BoardMatrix[i][j+1] and BoardMatrix[i][j] != BLK): # If they are the same
                    BoardMatrix[i][j] = int(BoardMatrix[i][j]) * 2
                    ScoreNum += int(BoardMatrix[i][j]) 
                    BoardMatrix[i][j+1] = BLK

    if (direction == 2): # Right
        for i in range(4):
            for j in range(3, -1, -1):
                if (BoardMatrix[i][j] == BoardMatrix[i][j-1] and BoardMatrix[i][j] != BLK): # If they are the same
                    BoardMatrix[i][j] = int(BoardMatrix[i][j]) * 2
                    ScoreNum += int(BoardMatrix[i][j])                     
                    BoardMatrix[i][j-1] = BLK

    if (direction == 3): # Up
        for i in range(4):
            for j in range(3):
                if (InvertedBoard[i][j] == InvertedBoard[i][j+1] and InvertedBoard[i][j] != BLK): # If they are the same
                    InvertedBoard[i][j] = int(InvertedBoard[i][j]) * 2
                    ScoreNum += int(InvertedBoard[i][j])                    
                    InvertedBoard[i][j+1] = BLK
        BoardMatrix = InvertedBoard.T

    if (direction == 4): # Down
        for i in range(4):
            for j in range(3, -1, -1):
                if (InvertedBoard[i][j] == InvertedBoard[i][j-1] and InvertedBoard[i][j] != BLK): # If they are the same
                    InvertedBoard[i][j] = int(InvertedBoard[i][j]) * 2
                    ScoreNum += int(InvertedBoard[i][j])                     
                    InvertedBoard[i][j-1] = BLK
        BoardMatrix = InvertedBoard.T


def UpdateTiles():
    global BoardMatrix
    canvas.delete("tile")
    for i in range(4):
        for j in range(4):
            if (BoardMatrix[i][j] != BLK): SpawnTile(BoardXMatrix[i][j], BoardYMatrix[i][j], BoardMatrix[i][j])

    
def RunGameFrame(direction):
    global ScoreNum
    print("hi")
    if (True):
        print("yay")
        MoveTiles(direction) # Move The Tiles
        MergeTiles(direction) # Merge Like Tiles
        MoveTiles(direction) # Move Tiles over any open space that may have been created while merging
        if (CheckForEmpty()):
            SpawnRandomTile()
        UpdateTiles()
        canvas.itemconfig(Score, text=ScoreNum)
#******************Run Functions From Key Press**************
    
def LeftKey(event):
    RunGameFrame(1)
    
def RightKey(event):
    RunGameFrame(2)
    
def UpKey(event):
    RunGameFrame(3)

def DownKey(event):
    RunGameFrame(4)

    
#*******************GAME GUI STUFF*************************

#Background
BkgdGrid = canvas.create_rectangle(125, 180, 625, 680, fill="#9F9F9F")
canvas.tag_lower("BkgdGrid")

#Individual Boxs
BkgdBox01 = canvas.create_rectangle(145, 200, 245, 300, fill="#C2C0B8", outline="")
BkgdBox02 = canvas.create_rectangle(265, 200, 365, 300, fill="#C2C0B8", outline="")
BkgdBox03 = canvas.create_rectangle(385, 200, 485, 300, fill="#C2C0B8", outline="")
BkgdBox04 = canvas.create_rectangle(505, 200, 605, 300, fill="#C2C0B8", outline="")
BkgdBox05 = canvas.create_rectangle(145, 320, 245, 420, fill="#C2C0B8", outline="")
BkgdBox06 = canvas.create_rectangle(265, 320, 365, 420, fill="#C2C0B8", outline="")
BkgdBox07 = canvas.create_rectangle(385, 320, 485, 420, fill="#C2C0B8", outline="")
BkgdBox08 = canvas.create_rectangle(505, 320, 605, 420, fill="#C2C0B8", outline="")
BkgdBox09 = canvas.create_rectangle(145, 440, 245, 540, fill="#C2C0B8", outline="")
BkgdBox10 = canvas.create_rectangle(265, 440, 365, 540, fill="#C2C0B8", outline="")
BkgdBox11 = canvas.create_rectangle(385, 440, 485, 540, fill="#C2C0B8", outline="")
BkgdBox12 = canvas.create_rectangle(505, 440, 605, 540, fill="#C2C0B8", outline="")
BkgdBox13 = canvas.create_rectangle(145, 560, 245, 660, fill="#C2C0B8", outline="")
BkgdBox14 = canvas.create_rectangle(265, 560, 365, 660, fill="#C2C0B8", outline="")
BkgdBox15 = canvas.create_rectangle(385, 560, 485, 660, fill="#C2C0B8", outline="")
BkgdBox16 = canvas.create_rectangle(505, 560, 605, 660, fill="#C2C0B8", outline="")
               
    
#****************************Lets Play!!!************************

#Bind Keys
master.bind_all('<Left>', LeftKey)
master.bind_all('<Right>', RightKey)
master.bind_all('<Up>', UpKey)
master.bind_all('<Down>', DownKey)
      
#the game loop
PlayGame = True
while PlayGame:




    #updateGUI
    master.update_idletasks()
    master.update()
        

