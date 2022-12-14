# code from https://github.com/KacperMayday/Snake-Genetic-Algorithm/blob/master/genetics.py

"""Configuration file containing global variables and hyperparameters.
Constants
---------
SCREENWIDTH, SCREENHEIGHT : int
    Screen resolution parameters. For training purpose I recommend setting
    as small values as possible to make the process faster.
TICKRATE: int
    Indicates maximum frames per second. For training set to very high value,
    otherwise 30-60 is recommended.
VELOCITY : int
    Number of pixels snake moves each frame.
SIZE : int
    Size in pixels of apple and every snake's segment. Size is equal to velocity
    to achieve grid effect.
POPULATION_SIZE : int
    Size of population in each generation. Used in genetic algorithm.
PARENTS_SIZE : int
    Number of best parents chosen from each population. Must be even and a divisor
    of population_size.
IDLE_TIME : int
    Time in millisecond for each apple catch. Prevents snakes looping to infinity.
MUTATION_RATE : int
    Maximum per mile change during mutation.
MUTATION_FREQUENCY : int
    Mutation frequency per cent.
CROSSING_PROBABILITY : int
    Probability of exchanging each chromosome with second parent during crossing_over stage.
EPOCHS : int
    Number of epochs during training. Set to 1 if you want to enter show mode.
WIN_MAX, WIN_MEAN : int
    Winning conditions, program stops upon reaching them.
"""

SCREENWIDTH = 50 * 12
SCREENHEIGHT = 50 * 12
TICKRATE = 30
VELOCITY = 1 * 12
SIZE = VELOCITY
POPULATION_SIZE = 100
PARENTS_SIZE = 10
IDLE_TIME = 2000 * 3
MUTATION_RATE = 50
MUTATION_FREQUENCY = 25
CROSSING_PROBABILITY = 10
EPOCHS = 1
WIN_MAX = 75
WIN_MEAN = 50