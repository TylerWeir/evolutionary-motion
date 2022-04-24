"""
agnet.py

Reprsents an agent operating in the simulated environment. Each agent contains a 
unique instance of an evolutionary neural network to control its movements.

Large amounts of state will be kept in the objects such as positions, orientations, 
velocities.

**NOTE: See the flywheight design pattern. It may be of use, though it is 
typically used when there are about 1e5 objects or more

see here for a csgo example: https://www.geeksforgeeks.org/flyweight-design-pattern/?msclkid=055e8a0cc06411ec91c2bef75e157f9d
another helpful source: https://sourcemaking.com/design_patterns/flyweight/python/1#:~:text=Code%20examples%20%20%20Java%20%20%20Flyweight,%20Flyweight%20in%20Python%20%20%20%20?msclkid=b056bba6c06411ec844b7bb5a3f5ef16

"""
import abc
import pygame
from pygame.math import Vector2
from body import Skeleton
from neural_net import NeuralNet
from math import atan2, degrees, pi, cos, sin, tanh
from activations import *
from scorer import Scorer

class Agent():
    """Agent defines a pole balancing entity. Each agent is made
    up a scoring object, a neural net, and a skeleton."""

    def __init__(self):
        """Defualt constructor. Defines an agent with a random 
        neural net.

        Returns: None
        """
        # An abstract position which is later
        # mapped to the center of the screen as zero.
        self.pos = Vector2((0,0))
        # self.x = 0
        # self.y = 0

        self.vel = Vector2((0,0))

        self.move_strength = 0.1 # how strong the force is when the player tries to move

        # Define the skeleton backing the agent
        points = [(0, 0), (0, -160)]
        sticks = [(0,1)]
        self.skeleton = Skeleton(points, sticks)

        # Define a score keeper for the agent
        self.scorer = Scorer()
        self.score = None

        # Define a NeuralNet for the agent
        self.net = NeuralNet(1, 1, sigmoid)
        self.net.add_hidden_layer(3, sigmoid)


    def move(self, x):
        """Moves the agent by the indicated amount on the x axis

        Parameters:
        - x (number): The horizontal distance to move

        Returns: None
        """

        # move the base
        self.pos.x += x
        self.pos.x += self.net.evaluate([-100])[0]

        # make the skeleton base match the agent
        self.skeleton.force_pos(0, self.pos)

    
    def apply_force(self, x_force):
        """Applies a force to the agent

        Parameters:
        - x_force (number): The force to move the agent with along the x-axis (can be negative)

        Returns: None
        """

        self.vel.x += x_force * self.move_strength
        # friction would go here though I think that's handled elsewhere
        self.move(self.vel.x)


    def update(self, delta_t):
        """Updates the agent given the time step.

        Parameters:
        - delta_t (float): The number of seconds that have passed since
                           the last frame.
        """

        # only update if the pole is airborne
        if not self.scorer.is_done():
            # get the direction of effort
            effort_vector = self.net.evaluate(np.array([0,]))
            move_force = tanh(effort_vector[0])
            self.apply_force(move_force)
            self.skeleton.move(delta_t)
            self.scorer.update(self.skeleton)

        # Assign the score if done updating and no score yet
        elif self.score == None:
            self.score = self.scorer.get_score()
            print("The agent's score is: ", self.score)


    def __draw_pole(self, canvas):

        # get the end points of the skeleton
        pt1 = self.skeleton.points[0]
        pt2 = self.skeleton.points[1]
        delta = pt2 - pt1

        radius = 3 
        length = pt1.distance_to(pt2)

        # TODO this needs refactoring
        width = canvas.get_width()
        height = canvas.get_height()
        base_pos = (self.pos.x + width/2, self.pos.y + height*2/3, 40, 20)
        
        # Find the angle of rotation
        rads = atan2(delta.y, delta.x)
       
        # This is how new points are calculated 
        # new_x_point = old_x_point * cos(Angle) - old_y_point * sin(Angle);
        # new_y_point = old_y_point * cos(Angle) + old_x_point * sin(Angle);
        sin_rads = sin(rads)
        cos_rads = cos(rads)

        x1 = radius * sin_rads
        x2 = -radius * sin_rads
        x3 = length * cos_rads - radius * sin_rads
        x4 = length * cos_rads + radius * sin_rads
        
        y1 = -radius * cos_rads
        y2 = radius * cos_rads
        y3 = radius * cos_rads + length * sin_rads
        y4 = -radius * cos_rads + length * sin_rads

        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        # map the offset through the points
        points = [(x + base_pos[0], y + base_pos[1]) for (x, y) in points]
        
        pygame.draw.polygon(canvas, (226, 41, 55), points)


    def draw(self, canvas):
        """Draws the agent to the given canvas.

        Parameters:
        - canvas (pygame.surface): A pygame surface to draw onto.

        Returns: None
        """

        # Draw relative to window size
        width = canvas.get_width()
        height = canvas.get_height()

        base_pos = (self.pos.x + width/2 - 20, self.pos.y + height*2/3 - 10, 40, 20)
        pygame.draw.rect(canvas, (39, 39, 47), base_pos, 0)

        self.__draw_pole(canvas)

        # For now also draw the skeleton
        #self.skeleton.draw(canvas)
