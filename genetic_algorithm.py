# code from https://github.com/KacperMayday/Snake-Genetic-Algorithm/blob/master/genetics.py
from random import randint

import torch
import torch.nn as nn

import config as cfg


def sort_best(score_array):
    """Determines which networks will be used in genetic algorithm.
    This function takes scores list of current generation and returns best
    network's IDs in ascending order.
    
    Parameters
    ----------
    score_array : list
        unsorted list of scores achieved by current generation
    Returns
    -------
    best_scores : list
        list of best neural networks' IDs
    """

    best_scores = [0] * cfg.PARENTS_SIZE
    for it in range(cfg.PARENTS_SIZE):
        best_scores[it] = score_array.index(max(score_array))
        score_array[best_scores[it]] = -1
    best_scores.sort()
    return best_scores


def save_best(list_of_bests):
    """Saves best models in the first N files in data directory, where N is
    equal to cfg.PARENTS_SIZE.
    Parameter
    ---------
    list_of_bests : list
        list of best networks' IDs
    """

    for iterator in range(len(list_of_bests)):
        model_file = 'data/{}.pt'.format(list_of_bests[iterator])
        temp = Brain()
        temp.load_state_dict(torch.load(model_file))
        torch.save(temp.state_dict(), 'data/{}.pt'.format(iterator))


def crossing_over(first_parent, second_parent):
    """Randomly exchanges chromosomes between parents.
    Each value from each layer in model's parameters is a chromosome which has
    a chance to be replaced, where probability is defined by cfg.CROSSING_PROBABILITY.
    Parameters
    ----------
    first_parent, second_parent : obj
        neural network objects
    Returns
    -------
    child : obj
        new neural network which is the result of combining parents' networks together
    """

    child = Brain()
    for layer_name, _ in child.named_parameters():
        child_params = child.state_dict()[layer_name]
        first_params = first_parent.state_dict()[layer_name]
        second_params = second_parent.state_dict()[layer_name]
        for tensor in range(len(child_params)):
            try:
                for value in range(len(child_params[tensor])):
                    probability = randint(1, 100)
                    if probability <= cfg.CROSSING_PROBABILITY:
                        child_params[tensor][value] = second_params[tensor][value]
                    else:
                        child_params[tensor][value] = first_params[tensor][value]

            except TypeError:
                probability = randint(1, 100)
                if probability <= cfg.CROSSING_PROBABILITY:
                    child_params[tensor] = second_params[tensor]
                else:
                    child_params[tensor] = first_params[tensor]

        child.state_dict()[layer_name] = child_params

    return child


def mutation(model):
    """Adds noise to model's parameters.
    Every value in model's parameters has a chance to be altered by random percent.
    Because weight tensor is one more level "nested" than bias tensor, both should
    be handled in slightly different way.
    Parameter
    ---------
    model : obj
        neural network which parameters are to be altered
    Returns
    -------
    model : obj
        altered neural network
    """

    for layer_name, _ in model.named_parameters():
        layer_params = model.state_dict()[layer_name]
        for tensor in range(len(layer_params)):
            try:  # when tensor is weight tensor
                for value in range(len(layer_params[tensor])):
                    probability = randint(1, 100)
                    change = randint(-cfg.MUTATION_RATE, cfg.MUTATION_RATE)
                    if probability <= cfg.MUTATION_FREQUENCY:
                        layer_params[tensor][value] = layer_params[tensor][value] \
                                                      + layer_params[tensor][value] \
                                                      * (change / 1000)

            except TypeError:  # when tensor is bias tensor
                probability = randint(1, 100)
                change = randint(-cfg.MUTATION_RATE, cfg.MUTATION_RATE)
                if probability <= cfg.MUTATION_FREQUENCY:
                    layer_params[tensor] = layer_params[tensor] + layer_params[tensor] * (change / 1000)
        model.state_dict()[layer_name] = layer_params
    return model


def breeding(first_parent, second_parent, file_number):
    """Performs breeding between given pair of individuals.
    Creates set of individuals by combining parents' chromosomes
    and saves offset to data directory. Because it matters which parent
    is first, two situations must be performed each producing half of
    the final offset.
    Parameters
    ----------
    first_parent : obj
        first parent neural network object
    second_parent : obj
        second parent neural network object
    file_number : int
        file number where offset is saved
    Returns
    -------
    file_number : int
        next free file number ready to be used
    """

    half_offset = (cfg.POPULATION_SIZE - cfg.PARENTS_SIZE) // cfg.PARENTS_SIZE

    for iterator in range(half_offset):
        child = crossing_over(first_parent, second_parent)
        child = mutation(child)
        torch.save(child.state_dict(), 'data/{}.pt'.format(file_number))
        file_number += 1

        child = crossing_over(second_parent, first_parent)
        child = mutation(child)
        torch.save(child.state_dict(), 'data/{}.pt'.format(file_number))
        file_number += 1

    return file_number


def mating():
    """Chooses pairs of individuals for breeding."""

    counter = cfg.PARENTS_SIZE
    for it in range(0, cfg.PARENTS_SIZE, 2):
        first = Brain()
        first.load_state_dict(torch.load('data/{}.pt'.format(it)))
        second = Brain()
        second.load_state_dict(torch.load('data/{}.pt'.format(it + 1)))
        counter = breeding(first, second, counter)

# Here's a network that we could potentially use
class Brain(nn.Module):
    """Neural Network class to control snake movement.
    Attributes
    ----------
    in_nodes : int
        number of input nodes / features for the network
    hidden_nodes : int
        number of hidden nodes
    out_nodes : int
        number of output nodes, corresponds to four main directions
    net : obj
        object representing neural network architecture
    Methods
    -------
    forward(inputs)
        returns the output array of the network, where each element corresponds
        to each direction: [up, right, down, left]. Maximum value is converted
        to one and the rest to zero
    """

    def __init__(self):
        super(Brain, self).__init__()

        self.in_nodes = 48
        self.hidden_nodes1 = 36
        self.hidden_nodes2 = 28
        self.out_nodes = 4
        
        self.net = nn.Sequential(nn.Linear(self.in_nodes, self.hidden_nodes1),
                                 nn.ReLU(),
                                 nn.Linear(self.hidden_nodes1, self.hidden_nodes2),
                                 nn.ReLU(),
                                 nn.Linear(self.hidden_nodes2, self.out_nodes),
                                 nn.Sigmoid())

    def forward(self, inputs):
        """Model's forwarding method which produces outputs.
        Outputs array in one-hot meaning that every element is binary value
        and only one element is equal 1. Position of 1 determines direction
        which snake will follow.
        Parameter
        ---------
        inputs : list
            list of inputs gathered by Game(). Check Game's get_inputs method
            for more information
        Returns
        -------
        outputs : list
            one-hot list representing chosen next move direction
        """

        inputs = torch.tensor(inputs).float()

        outputs = [0] * 4

        net_product = self.net(inputs).tolist()
        outputs[net_product.index(max(net_product))] = 1

        return outputs
