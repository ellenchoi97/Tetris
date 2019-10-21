import pygame, time
from Board import *
from Block import *

pygame.init()
screen = pygame.display.set_mode((500, 500))

##### OBJECTS #####
board = Board()             #Create a new board
block = Block(screen)       #Create a new block

##### CONSTANTS #####
WHITE = (255, 255, 255)     #RGB values for white
BLACK = (0, 0, 0)           #RGB values for black
SIDE = 0.12                 #The counter limit for moving left/right

##### BOOLEANS #####
leftDown = False            #If the left arrow key is held down
rightDown = False           #If the right arrow key is held down
fall = False                #If the block should soft drop
update = True               #If the scene should be updated
pause = False               #If the game is paused
done = False                #If the program is stopped

##### COUNTERS/TIMERS #####
normal_fall = 0.45           #The counter limit for a normal fall
fast_fall = 0.07              #The counter limit for a soft drop
lastSide = time.time()       #The previous time when the block moved left/right
lastFall = time.time()       #The previous time when the block moved down

##### FONT RELATED VARIABLES #####
theFont = pygame.font.SysFont("Arial", 32)
textSurface = theFont.render("", False, WHITE)

##### MISC VARIABLES #####
room = 1


##### GAME LOOP ######
while not done:

    #Check all events
    for event in pygame.event.get():

        #If the X button was clicked, end the game
        if event.type == pygame.QUIT:
            done = True
            continue

        #If a keyboard key was pressed
        elif event.type == pygame.KEYDOWN:

            #If Escape was pressed, end the game
            if event.key == pygame.K_ESCAPE:
                done = True
                continue

            #If game intro screen, accept any key to start the game
            if room == 1:
                room += 1
                textSurface = theFont.render("Score: 0", False, WHITE)
                update = True
                continue

            #If P was pressed, pause/un-pause the game
            if event.key == pygame.K_p:
                pause = not pause
                update = True
                continue

            #If the up arrow key was pressed
            if event.key == pygame.K_UP:
                
                #Rotate the block
                block.rotate()

                '''
                If rotating the block moves it out of the board,
                bring the block back in
                '''
                result = board.canMove(block.row, block.column, block.nextBlock)
                while not result[0]:
                    if result[1] == "left":
                        block.column += 1
                    elif result[1] == "right":
                        block.column -= 1
                    else:
                        break
                    result = board.canMove(block.row, block.column, block.nextBlock)
                update = True

            #If the down arrow key was pressed
            if event.key == pygame.K_DOWN:
                fall = True
                counter = 0

            #If the left arrow key was pressed
            elif event.key == pygame.K_LEFT:
                leftDown = True
                sideCounter = 0

            #If the right arrow key was pressed
            elif event.key == pygame.K_RIGHT:
                rightDown = True
                sideCounter = 0

        #If a keyboard key was released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fall = False
                counter = 0
            elif event.key == pygame.K_LEFT:
                leftDown = False
            elif event.key == pygame.K_RIGHT:
                rightDown = False

    if room == 2:
        #If the enough time passed to move left/right            
        if not pause and time.time() - lastSide > SIDE:
            
            #If the left arrow key is held down and the block can move left
            if leftDown and board.canMove(block.row, block.column - 1, block.nextBlock)[0]:
                block.moveLeft()
                update = True

            #If the right arrow key is held down and the block can move right
            elif rightDown and board.canMove(block.row, block.column + 1, block.nextBlock)[0]:
                block.moveRight()
                update = True

            #Get the current time
            lastSide = time.time()

        #If it is time for the block to fall based on its fall mode
        if not pause and ((not fall and time.time() - lastFall > normal_fall) or
            (fall and time.time() - lastFall > fast_fall)):

            #If the block can fall down
            if board.canMove(block.row + 1, block.column, block.nextBlock)[0]:
                block.moveDown()

            #Otherwise
            else:
                #Update the board matrix and update the score
                death = not board.fillBoard(block.row, block.column,
                                           block.color, block.nextBlock)
                textSurface = theFont.render("Score: " + str(board.score), False, WHITE)

                #If placing the block did not end in death
                if not death:

                    #Get the next block
                    block.newBlock()

                    '''
                        Move the block at most twice upwards if there are blocks
                        taking up the first and/or second row
                    '''
                    for _ in range(2):
                        result = board.canMove(block.row, block.column, block.nextBlock)
                        if not result[0] and result[1] == "up":
                            block.row -= 1

                    #Increase the speed of the fall
                    if normal_fall > 0.07:
                        normal_fall -= int(board.score / 280) * 0.00001

                        #If normal fall is as fast as soft drop, then stop soft drops
                        if normal_fall < fast_fall:
                            fast_fall = normal_fall

                else:
                    room += 1

            #Get the current time and update the screen
            lastFall = time.time()
            update = True

    #Draw current scene
    if update:
        
        #Set the background
        screen.fill(BLACK)

        #Scene for game intro
        if room == 1:
            textSurface = theFont.render("Press Any Key To Start", False, WHITE)
            bound = textSurface.get_rect()
            screen.blit(textSurface, ((500 - bound.width) / 2, 250))

        #Scene for game paused
        elif pause:
            textSurface = theFont.render("Game Paused", False, WHITE)
            bound = textSurface.get_rect()
            screen.blit(textSurface, ((500 - bound.width) / 2, 250))

        #Scene for gameplay
        elif room == 2:
            board.draw(screen)
            block.draw()
            screen.blit(textSurface, (0,0))

        #Scene for game over
        elif room == 3:
            img = pygame.image.load("game_over.jpg")
            screen.blit(img, (0, 100))
            bound = textSurface.get_rect()
            screen.blit(textSurface, ((500 - bound.width) / 2, 250))

        #Update the screen
        pygame.display.update()
        update = False
    
pygame.quit()
