"""Library contianing activation functions for use in neural 
networks.
Author: Tyler Weir
Date: Feb 23, 2022
"""
import numpy as np

def sigmoid(arg):
    """The sigmoid activation function returns the value of the 
    sigmoid function for the given argument value."""
    return 1/(1 + np.exp(-arg))

def relu(arg):
    """The Relu activation function returns 0 if the arg is less than
    0, and the identity function otherwise."""
    return max(0, arg)
