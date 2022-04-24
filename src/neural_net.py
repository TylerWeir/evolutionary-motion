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

import numpy as np
from activations import *

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
        self.activations = [None, tanh]


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


    def train(self, num_epochs, learning_rate):
        """Trains the net for `num_epochs` at `learning_rate`"""
        #TODO
        # this is not needed for our project
        return None


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
        return str(self.weights)


    def draw(self, canvas):
        """Draws a graph like representation of the current state of
        the neural network to the given tkinter canvas.  The gradient 
        represents the weights of the edges."""
        #TODO this is for tkinter

        #HARDCODED VALUES RN TODO
        nodesize = 40 
        node_vert_space = 10
        layerspace = 60 

        # Calculate the offset needed to align the middle of each 
        # node layer
        # First get the longest layer index
        longest_layer = 0
        for i, _ in enumerate(self.nodes):
            if len(self.nodes[i]) > len(self.nodes[longest_layer]):
                longest_layer = i
        
        longest_length = len(self.nodes[longest_layer])
        longest_height = longest_length*(nodesize+node_vert_space)
        longest_height -= node_vert_space

        # Store the node positions for reference when drawing the
        # edges.
        node_positions = []

        # First draw the nodes
        for i, _ in enumerate(self.nodes):
            length = len(self.nodes[i])
            height = length*(nodesize+node_vert_space)
            height -= node_vert_space

            diff = longest_height - height
            vert_offset = diff/2

            node_positions.append(self.nodes[i].tolist())

            for j, _ in enumerate(self.nodes[i]):
                x0 = i*(nodesize + layerspace)
                y0 = j*(nodesize + node_vert_space) + vert_offset
                x1 = x0 + nodesize
                y1 = y0 + nodesize
                fill = self.__calc_node_color(self.nodes[i][j])
                canvas.create_oval(x0, y0, x1, y1, fill=fill)
                node_positions[i][j] = (x0+nodesize/2, y0+nodesize/2)

        # Then draw the connections
        for i, _ in enumerate(self.weights): #weight layer
            for j, _ in enumerate(node_positions[i]): #node input
                x0 = node_positions[i][j][0] + nodesize/2
                y0 = node_positions[i][j][1]

                for k, _ in enumerate(node_positions[i+1]):
                    x1 = node_positions[i+1][k][0] - nodesize/2
                    y1 = node_positions[i+1][k][1]
                    canvas.create_line(x0, y0, x1, y1)
 

