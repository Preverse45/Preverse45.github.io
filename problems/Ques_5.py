#defines--------------------------------------------
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BUTTON_SPACE = 200
BUTTON_WIDTH = 5
BUTTON_HEIGHT = 5
TILE_X = 4
TILE_Y = 4
#---------------------------------------------------
CANVAS_BACKGROUND_COLOR = "lightblue"
BUTTON_BACKGROUND_COLOR = "black"
BUTTON_FOREGROUND_COLOR = "red"
TILE_COLOR = ["lightyellow", "yellow", "gold", "goldenrod", "rosybrown", "indianred", "salmon", "hotpink", "violetred", "firebrick1", "red"]
WIN_SCORE = 32
#---------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import random
import math

class Tile():
	m_Number = 0
	def __init__(self, topLeftX, topLeftY, topRightX, topRightY, textOnTile, canvas):
		if (textOnTile == WIN_SCORE):
			game.isRunning = False
			MsgBox = tk.messagebox.askquestion('Exit Application','You Won! (Press Ok To Exit Game)',icon = 'warning')
			if MsgBox == 'yes':
				game.isRunning = False

		power = math.log(textOnTile, 2)
		self.m_Number = textOnTile
		self.m_Canvas = canvas
		self.m_Rect = self.m_Canvas.create_rectangle(topLeftX, topLeftY, topRightX, topRightY, fill = TILE_COLOR[int(power) - 1])
		self.m_TileString = self.m_Canvas.create_text(topLeftX + (topRightX - topLeftX) / 2, 
												topLeftY + (topRightY - topLeftY) / 2, font = ("Pursia", 20), text=str(textOnTile))
		self.m_IsDestroyed = False

	def Translate(self, xpos, ypos):
		self.m_Canvas.move(self.m_Rect, xpos, ypos)
		self.m_Canvas.move(self.m_TileString, xpos, ypos)

	def Destroy(self):
		self.m_Canvas.delete(self.m_Rect)
		self.m_Canvas.delete(self.m_TileString)
		self.m_IsDestroyed = True

	def ChangeNumber(self, number):
		self.m_Number = number
		self.m_Canvas.itemconfig(self.m_TileString, text = str(self.m_Number))

class MainApplication(tk.Frame):
	windowStatus = True
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.pack(side = "top", fill = "both", expand = False)
		self.Setup()

	def Setup(self):
		self.m_Canvas = tk.Canvas(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT + BUTTON_SPACE)
		self.m_Canvas.pack()
		self.m_Canvas.config(background = CANVAS_BACKGROUND_COLOR)

	def callback():
		MainApplication.windowStatus = False

def CreateButtons(canvas):
	allButtons = {}
	x = BUTTON_WIDTH
	y = int(BUTTON_HEIGHT * (WINDOW_WIDTH / (WINDOW_HEIGHT + BUTTON_SPACE)))

	buttonUp = tk.Button(canvas, text = "UP", fg = BUTTON_FOREGROUND_COLOR, bg = BUTTON_BACKGROUND_COLOR, width = x, height = y, command = Game.upPressed)
	buttonWindow = canvas.create_window(WINDOW_WIDTH / 2, WINDOW_HEIGHT + BUTTON_SPACE / 3, window = buttonUp)

	buttonDown = tk.Button(canvas, text = "DOWN", fg = BUTTON_FOREGROUND_COLOR, bg = BUTTON_BACKGROUND_COLOR, width = x, height = y, command = Game.downPressed)
	buttonWindow = canvas.create_window(WINDOW_WIDTH / 2, WINDOW_HEIGHT + BUTTON_SPACE / 3 + (BUTTON_HEIGHT * 10), window = buttonDown)

	buttonLeft = tk.Button(canvas, text = "LEFT", fg = BUTTON_FOREGROUND_COLOR, bg = BUTTON_BACKGROUND_COLOR, width = x, height = y, command = Game.leftPressed)
	buttonWindow = canvas.create_window(WINDOW_WIDTH / 2 - (BUTTON_WIDTH * 10), WINDOW_HEIGHT + BUTTON_SPACE / 3 + (BUTTON_HEIGHT * 10), window = buttonLeft)

	buttonRight = tk.Button(canvas, text = "RIGHT", fg = BUTTON_FOREGROUND_COLOR, bg = BUTTON_BACKGROUND_COLOR, width = x, height = y, command = Game.rightPressed)
	buttonWindow = canvas.create_window(WINDOW_WIDTH / 2 + (BUTTON_WIDTH * 10), WINDOW_HEIGHT + BUTTON_SPACE / 3 + (BUTTON_HEIGHT * 10), window = buttonRight)

class Game():
	isRunning = True
	allTiles = {}
	tiles = []
	recSizeX = 0
	recSizeY = 0
	def __init__(self, canvas, *args, **kwargs):
		for x in range(0, TILE_X):
			tempList = {}
			for y in range(0, TILE_Y):
				tempList[y] = 0
			self.allTiles[x] = tempList
		self.allTiles[0][0] = 2
		self.allTiles[0][3] = 2
		self.CreateTiles(canvas)

		self.m_Canvas = canvas
		self.CreateTiles(self.m_Canvas)
		CreateButtons(canvas)
		self.recSizeX = WINDOW_WIDTH / TILE_X
		self.recSizeY = WINDOW_WIDTH / TILE_Y

	def MoveUp(self):
		for x in range(0, TILE_X):
			templist = []
			for y in range(0, TILE_Y):
				templist.append(self.allTiles[x][y])
			templist = Game.Compress(templist, len(templist))
			for y in range(0, TILE_Y - 1):
				if (templist[y] == templist[y+1]):
					templist[y] = templist[y] + templist[y+1]
					templist[y+1] = 0
			templist = Game.Compress(templist, len(templist))
			for y in range(0, TILE_Y):
				self.allTiles[x][y] = templist[y]

	def MoveDown(self):
		for x in range(0, TILE_X):
			templist = []
			for y in range(0, TILE_Y):
				templist.append(self.allTiles[x][y])
			templist = Game.Compress(templist, len(templist))
			templist.reverse()
			for y in range(TILE_Y - 1, -1, -1):
				if (templist[y] == templist[y-1]):
					templist[y] = templist[y] + templist[y-1]
					templist[y - 1] = 0
			templist = Game.Compress(templist, len(templist))
			templist.reverse()
			for y in range(0, TILE_Y):
				self.allTiles[x][y] = templist[y]

	def MoveLeft(self):
		for y in range(0, TILE_Y):
			templist = []
			for x in range(0, TILE_X):
				templist.append(self.allTiles[x][y])
			templist = Game.Compress(templist, len(templist))
			for x in range(TILE_X - 1, -1, -1):
				if (templist[x] == templist[x - 1]):
					templist[x] = templist[x] + templist[x - 1]
					templist[x - 1] = 0
			templist = Game.Compress(templist, len(templist))
			for x in range(0, TILE_Y):
				self.allTiles[x][y] = templist[x]

	def MoveRight(self):
		for y in range(0, TILE_Y):
			templist = []
			for x in range(0, TILE_X):
				templist.append(self.allTiles[x][y])
			templist = Game.Compress(templist, len(templist))
			templist.reverse()
			for x in range(0, TILE_X - 1):
				if (templist[x] == templist[x + 1]):
					templist[x] = templist[x] + templist[x+1]
					templist[x+1] = 0
			templist = Game.Compress(templist, len(templist))
			templist.reverse()
			for x in range(0, TILE_Y):
				self.allTiles[x][y] = templist[x]
	
	def Compress(arr, len):
		count = 0
		for i in range(len):
			if arr[i] != 0:
				arr[count] = arr[i] 
				count+=1
		while count < len: 
			arr[count] = 0
			count += 1
		return arr

	def Move(code):
		if (code == "UP"):
			game.MoveUp()
		if (code == "DOWN"):
			game.MoveDown()
		if (code == "LEFT"):
			game.MoveLeft()
		if (code == "RIGHT"):
			game.MoveRight()
		while True:
			isFull = True;
			for x in range(0, TILE_X):
				for y in range(0, TILE_Y):
					if (game.allTiles[x][y] == 0):
						isFull = False
			if (isFull):
				break

			randX = random.randint(0, TILE_X - 1)
			randY = random.randint(0, TILE_X - 1)
			if (game.allTiles[randX][randY] == 0):
				game.allTiles[randX][randY] = 2
				break
		game.CreateTiles(game.m_Canvas)
			

	def MoveToTile(self, tile, x, y, cx, cy):
		if (tile != 0 and x < TILE_X and y < TILE_Y):
			tile.Translate(self.recSizeX * abs(cx - x), self.recSizeY * abs(cy - y))


	def upPressed():
		Game.Move("UP")
	def downPressed():
		Game.Move("DOWN")
	def leftPressed():
		Game.Move("LEFT")
	def rightPressed():
		Game.Move("RIGHT")

	def DeleteTiles(self):
		for x in self.tiles:
			x.Destroy()
		self.tiles.clear()


	def CreateTiles(self, canvas):
		self.DeleteTiles()
		recSizeX = WINDOW_WIDTH / TILE_X
		recSizeY = WINDOW_WIDTH / TILE_Y

		for x in range(0, TILE_X):
			for y in range(0, TILE_Y):
				if (self.allTiles[x][y] != 0):
					self.tiles.append(Tile(x * recSizeX, y * recSizeY, (x + 1) * recSizeX, (y + 1) * recSizeY, self.allTiles[x][y], canvas))

if __name__ == "__main__":
	root = tk.Tk()
	root.protocol("WM_DELETE_WINDOW", MainApplication.callback)
	root.resizable(False, False)
	pop = MainApplication(root)

	game = Game(pop.m_Canvas)

	temp = 0

	while True:
		if (pop.windowStatus == False or game.isRunning == False):
			root.destroy()
			break
		root.update()
		root.update_idletasks()
