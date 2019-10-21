import pygame
import random

##### COLOR CONSTANTS #####
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 196, 245)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

#Dictionary of all block colors
colors = {"red": RED, "orange": ORANGE, "yellow": YELLOW,
          "green": GREEN, "light blue": LIGHT_BLUE, "blue": BLUE,
          "purple": PURPLE}

#J
type_1 = [[(0,0),(0,1),(1,1),(2,1)],
          [(0,0),(1,0),(0,1),(0,2)],
          [(0,0),(1,0),(2,0),(2,1)],
          [(0,2),(1,0),(1,1),(1,2)]]

#L
type_2 = [[(0,1), (1,1), (2,1), (2,0)],
          [(1,0), (1,1), (1,2), (2,2)],
          [(0,1), (1,1), (2,1), (0,2)],
          [(0,0), (1,0), (1,1), (1,2)]]

#S
type_3 = [[(0,1), (1,1), (1,0), (2,0)],
          [(1,0), (1,1), (2,1), (2,2)],
          [(0,2), (1,1), (1,2), (2,1)],
          [(0,0), (0,1), (1,1), (1,2)]]

#Z
type_4 = [[(0,0), (1,0), (1,1), (2,1)],
          [(2,0), (1,1), (2,1), (1,2)],
          [(0,1), (1,1), (1,2), (2,2)],
          [(0,1), (0,2), (1,0), (1,1)]]

#T
type_5 = [[(1,0), (0,1), (1,1), (2,1)],
          [(1,0), (1,1), (1,2), (2,1)],
          [(0,1), (1,1), (2,1), (1,2)],
          [(0,1), (1,0), (1,1), (1,2)]]

#I
type_6 = [[(0,1), (1,1), (2,1), (3,1)],
          [(2,0), (2,1), (2,2), (2,3)],
          [(0,2), (1,2), (2,2), (3,2)],
          [(1,0), (1,1), (1,2), (1,3)]]

#O
type_7 = [[(0,0), (0,1), (1,0), (1,1)],
          [(0,0), (0,1), (1,0), (1,1)],
          [(0,0), (0,1), (1,0), (1,1)],
          [(0,0), (0,1), (1,0), (1,1)]]

##### Class for the Tetris blocks #####
class Block:        
    def __init__(self, drawScreen):
        self.screen = drawScreen    #The Surface for the game
        self.blockList = []         #The order for the next set of blocks
        self.blockIndex = 6         #The index for blockList
        self.newBlock()

    def newBlock(self):
        self.index = 0              #The index of the block's rotation
        self.row = 0                #The row that the block is in
        self.column = 4             #The column that the block is in

        '''
            If the current block is the last block in the set, randomly
            select a new order for the next set of blocks
        '''
        if self.blockIndex == 6:
            self.blockList = [i + 1 for i in range(7)]
            random.shuffle(self.blockList)

        #Get the index of the next block in the set
        self.blockIndex = (self.blockIndex + 1) % 7

        #Get the list of square coordinates for the new block
        if self.blockList[self.blockIndex] == 1:
            self.nextBlock = type_1[self.index]
            self.color = "red"
        elif self.blockList[self.blockIndex] == 2:
            self.nextBlock = type_2[self.index]
            self.color = "orange"
        elif self.blockList[self.blockIndex] == 3:
            self.nextBlock = type_3[self.index]
            self.color = "yellow"
        elif self.blockList[self.blockIndex] == 4:
            self.nextBlock = type_4[self.index]
            self.color = "green"
        elif self.blockList[self.blockIndex] == 5:
            self.nextBlock = type_5[self.index]
            self.color = "light blue"
        elif self.blockList[self.blockIndex] == 6:
            self.row = -1
            self.nextBlock = type_6[self.index]
            self.color = "blue"
        elif self.blockList[self.blockIndex] == 7:
            self.nextBlock = type_7[self.index]
            self.color = "purple"

    #The function to rotate the block
    def rotate(self):

        #Get the index of the next rotation
        self.index = int(self.index + 1) % 4

        #Get the list of square coordinates for the next rotation
        if self.blockList[self.blockIndex] == 1:
            self.nextBlock = type_1[self.index]
        elif self.blockList[self.blockIndex] == 2:
            self.nextBlock = type_2[self.index]
        elif self.blockList[self.blockIndex] == 3:
            self.nextBlock = type_3[self.index]
        elif self.blockList[self.blockIndex] == 4:
            self.nextBlock = type_4[self.index]
        elif self.blockList[self.blockIndex] == 5:
            self.nextBlock = type_5[self.index]
        elif self.blockList[self.blockIndex] == 6:
            self.nextBlock = type_6[self.index]
        elif self.blockList[self.blockIndex] == 7:
            self.nextBlock = type_7[self.index]

    #The function to move the block to the left
    def moveLeft(self):
        self.column -= 1

    #The function to move the block to the right
    def moveRight(self):
        self.column += 1

    #The function to move the block down
    def moveDown(self):
        self.row += 1

    #The function to draw the block
    def draw(self):
        
        #For all the block's square
        for i in range(len(self.nextBlock)):

            #Calculate the square's "world" coordinates
            x = 20*(self.nextBlock[i][0] + self.column) + 150
            y = 20*(self.nextBlock[i][1] + self.row) + 50

            #Draw the square if it is on the board
            if y >= 50:
                pygame.draw.rect(self.screen, colors[self.color],
                                 (x, y, 19.5, 19.5))
