# AI for Games - Beat the Snake game
# Training the AI

# Importing the libraries
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import os
from genetic_algorithm import Brain
import genetic_algorithm as ga

# Defining the parameters
memSize = 60000
batchSize = 32
learningRate = 0.0001
gamma = 0.9
nLastStates = 4

filepathToSave = 'model2.h5'

# Creating the Environment, the Brain and the Experience Replay Memory
env = Environment(0)
brain = Brain()

# Making a function that will initialize game states
def resetStates():

    currentState = env.getVision()
    
    return currentState, currentState

# code from https://github.com/Chrispresso/SnakeAI/blob/master/snake.py
def calculate_fitness(env):
    # Give positive minimum fitness for roulette wheel selection
    env.snakeFitness = (env.snakeMoves) + ((2**env.snakeScore) + (env.snakeScore**2.1)*500) - (((.25 * env.snakeMoves)**1.3) * (env.snakeScore**1.2))
    env.snakeFitness = max(env.snakeFitness, .1)


# Starting the main loop
scores = list()
maxNCollected = 0
nCollected = 0.
totNCollected = 0

while True:
    # Resetting the environment and game states
    env.reset()
    currentState, nextState = resetStates()
    gameOver = False
    
    # Starting the second loop in which we play the game and teach our AI
    while not gameOver: 
        
        # Choosing an action to play
        actions = brain.forward(currentState)
        action = np.argmax(actions)
        
        # Updating the environment
        state, gameOver = env.step(action)

        vision = env.getVision()
        
        nothing = input("Press Enter to continue...")
        
        # TODO: track the snake's fitness
        
        # Checking whether we have collected an apple and updating the current state
        if env.collected:
            nCollected += 1
        
        currentState = nextState
    
    # Checking if a record of apples eaten in a around was beaten and if yes then saving the model
    if nCollected > maxNCollected and nCollected > 2:
        maxNCollected = nCollected
        model.save(filepathToSave)
    
    totNCollected += nCollected
    nCollected = 0
