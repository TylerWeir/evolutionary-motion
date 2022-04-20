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
        self.intrinsic_state = None

        # Define the skeleton backing the agent
        points = [(40, 300), (40, 290)]
        sticks = [(0,1)]
        self.skeleton = Skeleton(points, sticks)

    @abc.abstractmethod
    def operation(self, extrinsic_state):
        """Description"""
        # TODO: this is a placeholder function. It will likely be replaced with 
        # functions such as `move` or `draw` etc.

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

    def draw(self, canvas):
        # Draw relative to window size
        width = canvas.get_width()
        height = canvas.get_height()

        base_pos = (width/2 - 40, height*2/3 + 10, 40, 20)
        pygame.draw.rect(canvas, (39, 39, 47), base_pos, 0)
