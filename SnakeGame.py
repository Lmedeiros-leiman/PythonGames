import tkinter
import random

BoardDetails = {
    # use < and > operator for checks 
    'MaxCols': 24,
    'MaxRows': 20,
    'GameSpeed' : 1000 # in MilliSeconds
}


class Snake():
    NextSegment = None
    PrevSegment = None
    
    selectedMove = None
    lastMove = (0,1)
    
    alive = True
    
    Pos = {
        "Row": 2,
        "Col": 4,
    }
    
    
    def __init__(self, size = 3, PrevSegment = None):
        
        if PrevSegment != None:
            lastPos = PrevSegment.Pos
            
            self.Pos = {
                "Row": lastPos["Row"] - self.selectedMove[0],
                "Col": lastPos["Col"] - self.selectedMove[1],
            }
            self.PrevSegment = PrevSegment
        
        
        if (size > 0):
            nextBodyPart = Snake(size=size-1, PrevSegment=self)
            self.NextSegment = nextBodyPart
            nextBodyPart.PrevSegment = self
            
        pass
    
    def isOcupying(self,targetPos):
        current_segment = self
        while current_segment != None:
            if current_segment.Pos["Row"] == targetPos["Row"] and current_segment.Pos["Col"] == targetPos["Col"]:
                return True
            
            current_segment = current_segment.NextSegment
            pass
        
        return False
    
    def Move(self, check = True):
        if (self.alive == False):
            return False
        
        # if no move is selected, use the last move (forward by default)
        if self.selectedMove == None:
            self.selectedMove = self.lastMove
        
         # calculates the future position
        targetPos = {
        "Row": self.Pos["Row"] + self.selectedMove[0],
        "Col": self.Pos["Col"] + self.selectedMove[1],
        }
        
        # prevents from backing into itself 
        if self.NextSegment and targetPos["Col"] == self.NextSegment.Pos["Col"] and targetPos["Row"] == self.NextSegment.Pos["Row"]:
            self.selectedMove = self.lastMove
            targetPos = {
                "Row": self.Pos["Row"] + self.selectedMove[0],
                "Col": self.Pos["Col"] + self.selectedMove[1],
            }
        
        if (check and ( targetPos["Col"] )):
            if (self.isOcupying(targetPos)):
                print("You hit yourself.")
                
                self.alive = False
                return False
        
        currentPos = self.Pos.copy()
    
        #moves the head
        self.lastMove = self.selectedMove
        self.Pos = targetPos
        
        #moves the body
        if (self.NextSegment != None):
            self.NextSegment.MoveSegment(currentPos)
            
        return True
    def MoveSegment(self, newPos):
        currentPos = self.Pos.copy()
        
        self.Pos = newPos
        
        if (self.NextSegment != None):
            self.NextSegment.MoveSegment(currentPos)
        pass
    
    def Draw(self,canvas : tkinter.Canvas):
        
        
        maxHeight = canvas.winfo_height()
        maxWidth = canvas.winfo_width()
        
        X0 = self.Pos["Col"] * ( maxWidth / BoardDetails['MaxCols'] ) 
        X1 = (self.Pos["Col"]+1) * ( maxWidth / BoardDetails['MaxCols'] ) -2
        Y0 = self.Pos["Row"] * ( maxHeight / BoardDetails['MaxRows'] ) 
        Y1 = (self.Pos["Row"] + 1) * ( maxHeight / BoardDetails['MaxRows'] ) -2
        
        canvas.create_rectangle(X0,Y0,X1,Y1, fill="green" )
        
        if (self.PrevSegment == None):
            #draw the head
            canvas.create_oval(X0+2,Y0+2,X1-2,Y1-2, fill="yellow" )
            
            
            pass
        
        if (self.NextSegment != None):
            self.NextSegment.Draw(canvas)
        
        pass
    
    def Grow(self,amount = 1):
        
        lastPiece = self.NextSegment
        while lastPiece.NextSegment != None:
            lastPiece = lastPiece.NextSegment
            pass
        
        # Add new segments one by one
        for _ in range(amount):
            newSegment = Snake(size=0, PrevSegment=lastPiece)
            lastPiece.NextSegment = newSegment
            lastPiece = newSegment
        
        pass
        
    
    
    pass


class Food():
    Position = {
        "Row": 0,
        "Col": 0,
    }
    
    def __init__(self, player : Snake):
        self.setNewPosition(player)
        pass
    
    def setNewPosition(self,player : Snake):
        
        while True:
            newPosition = {
                "Row": int(random.random() * BoardDetails['MaxRows']),
                "Col": int(random.random() * BoardDetails['MaxCols']),
            }

            if not player.isOcupying(newPosition):
                self.Position = newPosition
                break
            
        pass

    def Draw(self,canvas : tkinter.Canvas):
        maxHeight = canvas.winfo_height()
        maxWidth = canvas.winfo_width()
        
        X0 = self.Position["Col"] * ( maxWidth / BoardDetails['MaxCols'] ) 
        X1 = (self.Position["Col"]+1) * ( maxWidth / BoardDetails['MaxCols'] ) -2
        Y0 = self.Position["Row"] * ( maxHeight / BoardDetails['MaxRows'] ) 
        Y1 = (self.Position["Row"] + 1) * ( maxHeight / BoardDetails['MaxRows'] ) -2
        
        canvas.create_rectangle(X0,Y0,X1,Y1, fill="red" )
        pass


def CreateWindow():
    Window = tkinter.Tk()
    Window.title("Snake Game")
    Window.geometry("800x600")
   
    GameCanvas = tkinter.Canvas(Window, background="white")
    GameCanvas.pack(fill=tkinter.BOTH, expand=True, padx=2, pady=2)
    Window.update()
    
    StartGame(GameCanvas)
    
    
    Window.mainloop()
    pass


def DrawGamePieces(canvas : tkinter.Canvas, player : Snake, food : Food):
    canvas.delete('all')
    
    Widht = canvas.winfo_width() / BoardDetails['MaxCols']
    Height = canvas.winfo_height() / BoardDetails['MaxRows']
    
    
    for row in range(0, BoardDetails['MaxRows']):
        canvas.create_line(0, row * Height ,canvas.winfo_width(), row * Height, width=2 ,fill="black")
        pass
    
    for col in range(0, BoardDetails['MaxCols']):
        canvas.create_line(col * Widht , 0 , col * Widht, canvas.winfo_height(), width=2 ,fill="black")
        pass
    
    player.Draw(canvas)
    food.Draw(canvas)

    pass


def StartGame(canvas : tkinter.Canvas):
    player = Snake()
    food = Food(player)
    
    DrawGamePieces(canvas,player, food)
    
    # redraws the frame if you resize the window.
    canvas.bind("<Configure>", lambda event:(DrawGamePieces(canvas,player, food)))
    
    def HandleKey(event):
        key_directions = {
            "Up": (-1, 0),
            "w": (-1, 0),
            
            "Down": (1, 0),
            "s": (1, 0),
            
            "Left": (0, -1),
            "a": (0, -1),
            
            "Right": (0, 1),
            "d": (0, 1)
        }
        if event.keysym in key_directions:
            player.selectedMove = (key_directions[event.keysym])
        
        pass
    
    canvas.bind_all("<Key>", HandleKey)
    
    
    
    def GameLoop():
        
        player.Move()
        if (player.isOcupying(food.Position)):
            player.Grow()
            food.setNewPosition(player)
        
        
        
        
        
        DrawGamePieces(canvas,player, food)
        
        
        
        
        
        
        
        # redraws the canvas and call the loop again.
        
        canvas.after(BoardDetails['GameSpeed'], GameLoop)
        pass
    GameLoop()
    
    pass

CreateWindow()