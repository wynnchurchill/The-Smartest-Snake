# AI for Games - Beat the Snake game
# Building the Environment

# Importing the libraries
import numpy as np
import pygame as pg

import config as cfg

# Initializing the Environment class
class Environment():
    
    def __init__(self, waitTime):
        
        # Defining the parameters
        self.width = 700            # width of the game window
        self.height = 700           # height of the game window
        self.nRows = 20             # number of rows in our board
        self.nColumns = 20          # number of columns in our board
        self.initSnakeLen = 2       # initial length of the snake
        self.waitTime = waitTime    # slowdown after taking an action
        self.snakeMoves = 0         # number of moves snake makes in lifetime
        self.snakeScore = 0         # total apples collected by snake
        self.snakeFitness = 0       # snake's calculated fitness
        
        if self.initSnakeLen > self.nRows / 2:
            self.initSnakeLen = int(self.nRows / 2)
        
        self.screen = pg.display.set_mode((self.width, self.height))
        
        self.snakePos = list()
        
        # Creating the array that contains mathematical representation of the game's board
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.5
            
        self.applePos = self.placeApple()
        
        self.drawScreen()
        
        self.collected = False
        self.lastMove = 0
    
    # Building a method that gets new, random position of an apple
    def placeApple(self):
        posx = np.random.randint(0, self.nColumns)
        posy = np.random.randint(0, self.nRows)
        while self.screenMap[posy][posx] == 0.5:
            posx = np.random.randint(0, self.nColumns)
            posy = np.random.randint(0, self.nRows)
        
        self.screenMap[posy][posx] = 1
        
        return (posy, posx)
    
    # Making a function that draws everything for us to see
    def drawScreen(self):
        
        self.screen.fill((0, 0, 0))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows

        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.screenMap[i][j] == 0.5 and self.snakePos[0] == (i,j):
                    pg.draw.rect(self.screen, (0, 255, 0), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 0.5:
                    pg.draw.rect(self.screen, (255, 255, 255), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 1:
                    pg.draw.rect(self.screen, (255, 0, 0), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                else:
                    pg.draw.rect(self.screen, (30, 30, 30), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                    
        pg.display.flip()
    
    # A method that updates the snake's position
    def moveSnake(self, nextPos, col):
        
        self.snakePos.insert(0, nextPos)
        
        if not col:
            self.snakePos.pop(len(self.snakePos) - 1)
        
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(len(self.snakePos)):
            self.screenMap[self.snakePos[i][0]][self.snakePos[i][1]] = 0.5
        
        if col:
            self.applePos = self.placeApple()
            self.collected = True
            
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1
    
    # The main method that updates the environment
    def step(self, action):
        # action = 0 -> up
        # action = 1 -> down
        # action = 2 -> right
        # action = 3 -> left
        
        # Resetting these parameters
        gameOver = False
        self.collected = False
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        snakeX = self.snakePos[0][1]
        snakeY = self.snakePos[0][0]
        
        # Checking if an action is playable and if not then it is changed to the playable one
        if action == 1 and self.lastMove == 0:
            action = 0
        if action == 0 and self.lastMove == 1:
            action = 1
        if action == 3 and self.lastMove == 2:
            action = 2
        if action == 2 and self.lastMove == 3:
            action = 3
        
        # Checking what happens when we take this action
        if action == 0:
            if snakeY > 0:
                if self.screenMap[snakeY - 1][snakeX] == 0.5:
                    gameOver = True
                elif self.screenMap[snakeY - 1][snakeX] == 1:
                    self.moveSnake((snakeY - 1, snakeX), True)
                elif self.screenMap[snakeY - 1][snakeX] == 0:
                    self.moveSnake((snakeY - 1, snakeX), False)
            else:
                gameOver = True
                
        elif action == 1:
            if snakeY < self.nRows - 1:
                if self.screenMap[snakeY + 1][snakeX] == 0.5:
                    gameOver = True
                elif self.screenMap[snakeY + 1][snakeX] == 1:
                    self.moveSnake((snakeY + 1, snakeX), True)
                elif self.screenMap[snakeY + 1][snakeX] == 0:
                    self.moveSnake((snakeY + 1, snakeX), False)
            else:
                gameOver = True
                
        elif action == 2:
            if snakeX < self.nColumns - 1:
                if self.screenMap[snakeY][snakeX + 1] == 0.5:
                    gameOver = True
                elif self.screenMap[snakeY][snakeX + 1] == 1:
                    self.moveSnake((snakeY, snakeX + 1), True)
                elif self.screenMap[snakeY][snakeX + 1] == 0:
                    self.moveSnake((snakeY, snakeX + 1), False)
            else:
                gameOver = True
        
        elif action == 3:
            if snakeX > 0:
                if self.screenMap[snakeY][snakeX - 1] == 0.5:
                    gameOver = True
                elif self.screenMap[snakeY][snakeX - 1] == 1:
                    self.moveSnake((snakeY, snakeX - 1), True)
                elif self.screenMap[snakeY][snakeX - 1] == 0:
                    self.moveSnake((snakeY, snakeX - 1), False)
            else:
                gameOver = True
        
        # Drawing the screen, updating last move and waiting the wait time specified
        self.drawScreen()
        self.lastMove = action
        
        pg.time.wait(self.waitTime)
        
        # Returning the new frame of the game and whether the game has ended or not
        return self.getVision(), gameOver
    
    # Making a function that resets the environment
    def reset(self):
        self.screenMap  = np.zeros((self.nRows, self.nColumns))
        self.snakePos = list()
        
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.5
        
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1
        
        self.lastMove = 0


    # code from https://github.com/KacperMayday/Snake-Genetic-Algorithm/blob/master/main.py
    def run_generation():
        """Runs all individuals in the population.
        Returns
        -------
        score_array : list
            list of scores achieved by each neural network in generation.
        """
        score_array = []
        #TODO: Complete this function so that it runs a certain number of snakes
        # and returns a list of their scores

        return score_array

    # looks in one line of sight, returning a list of 3 distances
    def look(self, x, y, x_step, y_step):
        results = [0,0,0]
        n_steps = 0
        while True:

            try:
                x += x_step
                y += y_step
                landing_square_val = self.screenMap[x][y]
                n_steps += 1

                if x < 0 or y < 0:
                    results[0] = n_steps
                    break

                # snake bod has been found (only the first snake body piece is counted)
                if landing_square_val == 0.5 and results[1] == 0:
                    results[1] = n_steps

                # food has been found
                if landing_square_val == 1:
                    results[2] = n_steps

            # the outside of the map has been found
            except IndexError:
                results[0] = n_steps + 1
                break

        return results

    # looks in 16 directions, returning a list of 48 distances
    def getVision(self):

        # the position of the head of the snake
        snake_x = self.snakePos[0][0]
        snake_y = self.snakePos[0][1]


        # the tuples of steps comprising the 16 directions
        directions = [(-1,-1), (-1,-2), (0,-1), (1,-2), (1,-1), (2,-1), (1,0), (2,1), (1,1), (1,2), (0,1), (-1,2), (-1,1), (-2,1), (-1,0), (-2,-1)]
        vision = []

        # look in all directions, appending the results to vision
        for x_step, y_step in directions:
 
            vision += self.look(snake_x, snake_y, x_step, y_step)

        # vision is a list containg 48 distances, in the order "outside, body, food, outside, body, food, etc."
        return vision

    def printCube(self, a):
        m = [
            [a[0], a[15], a[14], a[13], a[12]],
            [a[1], " ", " ", " ", a[11]],
            [a[2], " ", "????", " ", a[10]],
            [a[3], " ", " ", " ", a[9]],
            [a[4], a[5], a[6], a[7], a[8]]]

        # print the items in columns with a minimun width of 3
        for row in m:
            print(" ".join("{:<4}".format(item) for item in row))
    
    def printVision(self):
        vision = self.getVision()

        edge_vision = []
        body_vision = []
        food_vision = []

        # gets every third element of the list
        for element in vision[::3]:
            edge_vision.append(element)
        # gets every third element of the list, starting with the second element
        for element in vision[1::3]:
            body_vision.append(element)
        # gets every third element of the list, starting with the third element
        for element in vision[2::3]:
            food_vision.append(element)

        # prints the 16 elements in a ring, starting with the top left corner
        print("\nEdge vision:")
        self.printCube(edge_vision)
        print("\nBody vision:")
        self.printCube(body_vision)
        print("\nFood vision:")
        self.printCube(food_vision)




# Additional code, actually not mentioned in the book, simply enables you to play the game on your own if you run this "environment.py" file. 
# We don't really need it, that's why it was not mentioned. 
if __name__ == '__main__':        
    env = Environment(1)
    start = False
    direction = 0
    gameOver = False
    while True:
        state = env.screenMap
        pos = env.snakePos
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameOver = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not start:
                    start = True
                if event.key == pg.K_UP and direction != 1:
                    direction = 0
                elif event.key == pg.K_RIGHT and direction != 3:
                    direction = 2
                elif event.key == pg.K_LEFT and direction != 2:
                    direction = 3
                elif event.key == pg.K_DOWN and direction != 0:
                    direction = 1
        
        if start:
            _, gameOver = env.step(direction)
        if gameOver:
            env.reset()
            direction = 0
