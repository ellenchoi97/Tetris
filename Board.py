import pygame

##### COLOR CONSTANTS #####
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 196, 245)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# Dictionary for the block colors
colors = {"red": RED, "orange": ORANGE, "yellow": YELLOW,
          "green": GREEN, "light blue": LIGHT_BLUE, "blue": BLUE,
          "purple": PURPLE}

##### Class for the Tetris Board #####
class Board:
    def __init__(self):
        self.score = 0
        self.boardMat = []
        for _ in range(20):
            self.boardMat.append(['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'])

    #The function to determine if the block can move in the specified direction
    def canMove(self, nextRow, nextColumn, blockList):

        #For all the squares in the block
        for blockCoord in blockList:

            #Get the square's "board" coordinates
            squareRow = nextRow + blockCoord[1]
            squareCol = nextColumn + blockCoord[0]

            #If the square is on the board
            if squareRow >= 0:

                #If the square is past the last row
                if squareRow > 19:
                    return (False, "")

                #If the square is past the left border
                elif squareCol < 0:
                    return (False, "left")

                #If the square is past the right border
                elif squareCol > 9:
                    return (False, "right")

                #If the square is colliding with another block
                elif self.boardMat[squareRow][squareCol] != 'O':
                    return (False, "up")

        #Otherwise, the block can move
        return (True, "")

    #The function to fill the board matrix with where the block stops
    def fillBoard(self, row, column, color, blockList):

        #For all squares in the block
        for blockCoord in blockList:

            #Get the square's "board" coordinates
            squareRow = row + blockCoord[1]
            squareCol = column + blockCoord[0]

            #If the square is not on the board
            if squareRow < 0:
                return False

            #Set the board's space to the color of the block
            self.boardMat[squareRow][squareCol] = color

        #The indices of the rows that are complete
        rowsCleared = [0]

        #For all rows, append the row index if it is full
        for i in range(20):
            fullRow = True
            if 'O' not in self.boardMat[i]:
                rowsCleared.append(i)

        '''
            The offset for the number of rows skipped after dropping
            and the number of rows cleared
        '''
        numDrop = 1
        numRowsClear = len(rowsCleared) - 1

        #Drop the rows
        for i in range(numRowsClear, 0, -1):
            for j in range(rowsCleared[i] - 1, rowsCleared[i-1], -1):
                for k in range(10):
                    self.boardMat[j + numDrop][k] = self.boardMat[j][k]
            numDrop += 1

        #Empty the top rows for the number of rows cleared
        for i in range(0, numRowsClear):
            self.boardMat[i] = ['O','O','O','O','O',
                                'O','O','O','O','O']

        #Increase the score based on the number of rows cleared
        if numRowsClear == 1:
            self.score += 40
        if numRowsClear == 2:
            self.score += 100
        if numRowsClear == 3:
            self.score += 300
        if numRowsClear == 4:
            self.score += 1200

        #The game has not ended yet   
        return True

    #The function for drawing the board
    def draw(self, screen):

        #Draw the lines for the columns of the board
        column = 150
        while column <= 350:
            pygame.draw.line(screen, WHITE, (column, 50), (column, 450))
            column += 20

        #Draw the lines for the rows of the board
        row = 50
        while row <= 450:
            pygame.draw.line(screen, WHITE, (150, row), (350, row))
            row += 20

        #Fill in the non-empty spaces 
        for i in range(20):
            for j in range(10):
                if self.boardMat[i][j] != 'O':
                    pygame.draw.rect(screen, colors[self.boardMat[i][j]],
                                     (20 * j + 150, 20 * i + 50, 19.5, 19.5))

