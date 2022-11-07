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
    
    def __init__(self, iS = (100,100,3), lr = 0.0005):
        
        self.learningRate = lr
        self.inputShape = iS
        self.numOutputs = 4
        self.model = Sequential() 
        
        # Adding layers to the model
        self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = self.inputShape))
        
        self.model.add(MaxPooling2D((2,2)))
        
        self.model.add(Conv2D(64, (2,2), activation = 'relu'))
        
        self.model.add(Flatten())
        
<<<<<<< Updated upstream
        self.model.add(Dense(units = 256, activation = 'relu'))
        
=======
        self.model.add(Dense(units = 48, kernel_initializer='random_uniform', activation = 'relu', input_dim=input_dims))
        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))
        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))
        self.model.add(Dense(units = 64, kernel_initializer='random_uniform', activation = 'relu'))
>>>>>>> Stashed changes
        self.model.add(Dense(units = self.numOutputs))
        
        # Compiling the model
        self.model.compile(loss = 'mean_squared_error', optimizer = Adam(lr = self.learningRate))
    
    # Making a function that will load a model from a file
    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model
