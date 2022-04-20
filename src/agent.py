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

class AgentFactory:
    """
    Create and manage agents which are flyweight objects.
    Ensure that flyweigghts are shared properly. When a client 
    requests a flyweight, the FlyweightFactory object supplies an existing
    instance or creates one, if none exists."""

    def __init__(self):
        self.agents = {}

    def get_agent(self, key):
        try: 
            agent = self.agents[key]
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

    @abc.abstractmethod
    def operation(self, extrinsic_state):
        # TODO: this is a placeholder function. It will likely be replaced with 
        # functions such as `move` or `draw` etc. 
        pass

# Possible to make an interface through which flyweights can receive and act
# on extrinsic state using ABCMeta


class ConcreteAgent:
    """
    Implements the agent interface and add storage for intrinsic state if any.
    A ConcreteAgent object must be sharable. Any state it stores must be 
    intrinsic; that is, it must be independent of the ConcreteAgent's context."""

    def operation(self, extrinsic_state):
        pass

