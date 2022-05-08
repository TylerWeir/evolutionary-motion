"""
neural_net.py

Contains an evolutionary neural net of some sort used to determine agent
movement in the simulated environment. The perfomance of a given net will 
be determined via a scoreing function which evalutes how well a given agent
performs some task. Currently that task is balancing a pole.

Currently the plan is to implement the NEAT algorithm though we may begin 
by using a simpler algorithm.

Here are some interesting resources:
https://vtechworks.lib.vt.edu/bitstream/handle/10919/51904/LD5655.V855_1988.L362.pdf?msclkid=ee207556c05311ec9fd01f6badbd474c

"""

import pickle
import numpy as np
import pygame
from activations import *
from constants import *
import math
import os
import sys

class NeuralNet:
    """Represents a basic neural network."""

    def __init__(self, input_size, output_size, activation):
        # Fields to make reference easier
        self.input_size = input_size
        self.output_size = output_size

        # List of Numpy arrays to represent matrices holding 
        # weights of connections between nodes
        self.weights = [np.random.rand(input_size, output_size)]

        # List of Numpy arays representing vectors holding the 
        # activations of nodes
        self.nodes = [np.zeros(input_size), np.zeros(output_size)]

        # A list containing the activation function specified for 
        # each layer of nodes.  
        # Does the input layer use activations? TODO
        self.activations = [None, activation]

    @classmethod
    def net_from_file(cls, filepath):
        """Loads a network from a file path and returns it wrapped in a neural net instance."""

        # Check that the file exists
        if not os.path.exists(filepath):
            print("[Neural Net]: The file does not exist")
            sys.exit()

        # Load the network with the pickler
        with open(filepath, "rb") as f:
            saved_net = pickle.load(f)
        return saved_net


    def save(self, filepath):
        """Save this instance via the pickler."""
        
        # Write the file in binary mode
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    
    def copy(self):
        nn = NeuralNet(self.input_size, self.output_size, self.activations[1])
        nn.weights = [np.copy(x) for x in self.weights]
        nn.nodes = [np.copy(x) for x in self.nodes]
        nn.activations = [x for x in self.activations]
        return nn

    
    def noisy_copy(self, std_dev=1):
        nn = self.copy()
        
        for weight in nn.weights:
            weight += np.random.normal(0, std_dev, weight.shape)
        
        for layer in nn.nodes:
            layer += np.random.normal(0, std_dev, layer.shape)
        
        return nn


    def add_hidden_layer(self, size, activation):
        # Add layer to nodes 
        self.nodes.insert(-1, np.zeros(size))

        # Add activation function
        self.activations.insert(-1, activation)
    
        # Remove the last entry of weights and add the two 
        # new entries
        self.weights.pop()

        # Weights into the hidden layer
        into_layer = len(self.nodes[-3])
        self.weights.append(np.random.rand(size, into_layer) * 2 - 1)

        # Weights out of the hidden layer
        self.weights.append(np.random.rand(self.output_size, size) * 2 - 1)


    def evaluate(self, data):
        """Passes `data` into the input layer of the net and returns
        the activations of the output layer.
        data -- should be a flattened representation of the sample.
        """
        #TODO NO biasing yet

        # Apply the data values to the input layer 
        for i, _ in enumerate(data):
            self.nodes[0][i] = data[i]

        # Work layer by layer appling weights and calculating 
        # activation
        for i in range(1, len(self.nodes)):
            raw_acts = np.dot(self.weights[i-1], self.nodes[i-1])
            
            # Then apply the activation function to each element
            act_f = self.activations[i]
            actual_acts = [act_f(x) for x in raw_acts]
            
            # copy into the net
            for j, _ in enumerate(actual_acts):
                self.nodes[i][j] = actual_acts[j]

        # Return the activations of the output layer
        return self.nodes[-1][:]


    def __calc_node_color(self, value):
        """Helper function to calculate the hexvalue of a node color
        from it's activation value. Applied sigmoid to the activation
        for easy translation into a gradient."""

        # Use sigmoid to be on 0-1 scale
        sig_val = sigmoid(value)

        # Convert to rgb values
        red = int(255 - 255 * sig_val)
        green = int(255 - (255-red)/2)
        blue = red

        # Convert rgb to hex
        return('#%02x%02x%02x' % (red, green, blue))


    def __str__(self):
        return str(self.weights) + str(self.nodes) + str(self.activations)


    def __find_widest_layer(self):
        """Finds the index of the layer with the most neurons.
        
        Returns: The index of the layer with the most neurons.
        """
        longest_layer_idx = 0
        for i, _ in enumerate(self.nodes):
            if len(self.nodes[i]) > len(self.nodes[longest_layer_idx]):
                longest_layer_idx = i

        return longest_layer_idx


    def __get_weight_color(self, activation_value):
        x = math.tanh(0.5*activation_value)

        if x < 0:
            r_diff = NEGATIVE_COLOR[0] - MIDDLE_COLOR[0] 
            g_diff = NEGATIVE_COLOR[1] - MIDDLE_COLOR[1] 
            b_diff = NEGATIVE_COLOR[2] - MIDDLE_COLOR[2] 

            r = NEGATIVE_COLOR[0] + r_diff * x
            g = NEGATIVE_COLOR[1] + g_diff * x
            b = NEGATIVE_COLOR[2] + b_diff * x

            return tuple((r, g, b))

        r_diff = POSITIVE_COLOR[0] - MIDDLE_COLOR[0]
        g_diff = POSITIVE_COLOR[1] - MIDDLE_COLOR[1]
        b_diff = POSITIVE_COLOR[2] - MIDDLE_COLOR[2]

        r = MIDDLE_COLOR[0] + r_diff * x
        g = MIDDLE_COLOR[1] + g_diff * x
        b = MIDDLE_COLOR[2] + b_diff * x

        return tuple((r, g, b))


    def __get_node_color(self, activation_value):
        x = abs(math.tanh(0.5*activation_value))
        return tuple((255*x, 255*x, 255*x))

    def draw(self, canvas):
        """Draws a graph like representation of the current state of
        the neural network to the given tkinter canvas.  The gradient 
        represents the weights of the edges."""

        # Calculate the offset needed to align the middle of each 
        # node layer
        # First get the longest layer index
        wide_index = self.__find_widest_layer()
        longest_length = len(self.nodes[wide_index])
        longest_height = longest_length * (NODE_RADIUS*2 + NODE_VERT_SPACE)
        longest_height -= NODE_VERT_SPACE

        # Offest for dawing the network
        net_width = len(self.nodes) * (NODE_RADIUS*2+LAYER_SPACE) - LAYER_SPACE
        x_offset = canvas.get_width()/2 - net_width/2
        y_offset = canvas.get_height()/4 - longest_height/2

        # Store the node positions for reference when drawing the
        # edges.
        node_positions = []

        # First draw the nodes
        for i, _ in enumerate(self.nodes):
            length = len(self.nodes[i])
            height = length * (NODE_RADIUS*2 + NODE_VERT_SPACE)
            height -= NODE_VERT_SPACE 

            diff = longest_height - height
            vert_offset = diff/2

            node_positions.append(self.nodes[i].tolist())

            for j, _ in enumerate(self.nodes[i]):
                x0 = i*(NODE_RADIUS*2 + LAYER_SPACE) + NODE_RADIUS
                y0 = j*(NODE_RADIUS*2 + NODE_VERT_SPACE) + vert_offset + NODE_RADIUS

                x0 += x_offset
                y0 += y_offset
                
                fill = self.__get_node_color(self.nodes[i][j])
                pygame.draw.circle(canvas, fill, (x0, y0), NODE_RADIUS)
                pygame.draw.circle(canvas, (0, 0, 0), (x0, y0), NODE_RADIUS, 1)
                
                node_positions[i][j] = (x0, y0)

        # Then draw the connections
        for i, _ in enumerate(self.weights): #weight layer
            for j, _ in enumerate(node_positions[i]): #node input
                x0 = node_positions[i][j][0] + NODE_RADIUS
                y0 = node_positions[i][j][1]

                for k, _ in enumerate(node_positions[i+1]):
                    x1 = node_positions[i+1][k][0] - NODE_RADIUS
                    y1 = node_positions[i+1][k][1]

                    fill = self.__get_weight_color(self.weights[i][k][j])

                    width = round(5 * abs(self.weights[i][k][j])) + 1

                    pygame.draw.line(canvas, fill, (x0, y0), (x1, y1), width=width)
