# AI for Games - Beat the Snake game
# Building the Brain

# Importing the libraries
# import tensorflow
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.optimizers import Adam

# Implementing Experience Replay
# Creating the Brain class
class Brain():
    
    # Change the shape of the input to match the 48, 16 directions, three pieces of information for each direction
    def __init__(self, input_dims = 48, lr = 0.0005):
        
        self.learningRate = lr
        self.inputShape = iS
        self.numOutputs = 4

        self.model = Sequential() 
        
        # This is all sequential neural network, and IDK what we should do with it. It's here for now.
        # Change to dense layers, instead of convolutional layers
        # self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = self.inputShape))
        
        # self.model.add(MaxPooling2D((2,2)))
        
        # self.model.add(Conv2D(64, (2,2), activation = 'relu'))
        
        # self.model.add(Flatten())
        
        self.model.add(Dense(units = 48, kernel_initializer='random_uniform', activation = 'relu', input_dim=input_dims))

        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))

        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))

        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))
        
        self.model.add(Dense(units = self.numOutputs))
        
        # Compiling the model
        # Once again, -\_(-_-)_/-
        self.model.compile(loss = 'mean_squared_error', optimizer = Adam(lr = self.learningRate))
    
    # Making a function that will load a model from a file
    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model
