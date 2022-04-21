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
from body import Skeleton
from math import atan2, degrees, pi, cos, sin

class AgentFactory:
    """
    Create and manage agents which are flyweight objects.
    Ensure that flyweigghts are shared properly. When a client 
    requests a flyweight, the FlyweightFactory object supplies an existing
    instance or creates one, if none exists."""

    def __init__(self):
        self.__agents = {}

    def get_agent(self, key):
        """Retreive an Agent matching the given key. If an agent with the key 
        does not exist, then a new agent will be created.

        Parameters:
        - key (int): The integer identifier of the agent

        Returns (ConcreteAgent): The agent matching the given key.
        """
        try:
            agent = self.__agents[key]
        except KeyError:
            agent = ConcreteAgent()
            self.__agents[key] = agent
        return agent

class Agent(metaclass=abc.ABCMeta):
    """
    Declare an interface through which flyweights can receive and act on 
    extrinsic state.
    """

    def __init__(self):
        # These are abstract positions which are later
        # mapped to the center of the screen as zero.
        self.x = 0
        self.y = 0

        # Define the skeleton backing the agent
        points = [(0, 0), (0, -160)]
        sticks = [(0,1)]
        self.skeleton = Skeleton(points, sticks)

    @abc.abstractmethod
    def operation(self, extrinsic_state):
        """Description"""
        # TODO: this is a placeholder function. It will likely be replaced with 
        # functions such as `move` or `draw` etc.

    @abc.abstractmethod
    def move(self, direction):
        """Moves the agent in the indicated direction.

        Parameters:
        - direction (int): The direction and magnitude to move with.

        Returns: None
        """

    def update(self, delta_t):
        """Updates the agent given the time step.

        Parameters:
        - delta_t (float): The number of seconds that have passed since 
                           the last frame."""

    @abc.abstractmethod
    def draw(self, canvas):
        """Draws the agent to the given canvas.

        Parameters:
        - canvas (pygame.surface): A pygame surface to draw onto.

        Returns: None
        """

# Possible to make an interface through which flyweights can receive and act
# on extrinsic state using ABCMeta

class ConcreteAgent(Agent):
    """
    Implements the agent interface and add storage for intrinsic state if any.
    A ConcreteAgent object must be sharable. Any state it stores must be 
    intrinsic; that is, it must be independent of the ConcreteAgent's context."""

    def operation(self, extrinsic_state):
        pass

    def move(self, direction):
        # move the base
        self.x += direction

        # make the skeleton base match the agent
        self.skeleton.force_pos(0, (self.x, self.y))

    def update(self, delta_t):
        self.move(0)
        #self.skeleton.move(delta_t)

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
        base_pos = (self.x + width/2, self.y + height*2/3, 40, 20)
        
        # Find the angle of rotation
        rads = -atan2(-delta.y, delta.x)
       
        # TODO refactor sin and cos
        x1 = radius * sin(rads)
        x2 = -radius * sin(rads)
        x3 = length * cos(rads) - radius * sin(rads)
        x4 = length * cos(rads) + radius * sin(rads)
        
        y1 = radius * cos(rads)
        y2 = radius * cos(rads)
        y3 = length * sin(rads) + radius*cos(rads)
        y4 = length * sin(rads) - radius*cos(rads)

        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        # map the offset through the points
        points = [(x + base_pos[0], y + base_pos[1]) for (x, y) in points]
        
        pygame.draw.polygon(canvas, (226, 41, 55), points)

    def draw(self, canvas):
        # Draw relative to window size
        width = canvas.get_width()
        height = canvas.get_height()

        base_pos = (self.x + width/2 - 20, self.y + height*2/3 - 10, 40, 20)
        pygame.draw.rect(canvas, (39, 39, 47), base_pos, 0)
        
        self.__draw_pole(canvas)

        # For now also draw the skeleton
        # self.skeleton.draw(canvas)
