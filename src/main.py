"""
main.py

This class is used to create an instance of the simulation. 
"""

from re import I
import environment
import graphics
import agent

class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self):
        """Default constuctor."""
        # Initialize the graphics
        self.screen = graphics.Graphics()

        # Initialize the agent factory and produce an agent
        self.agentFactory = agent.AgentFactory()
        self.agentFactory.get_agent(1)

    def run(self):
        """Runs the program."""
        while True:
            # Draw agent1
            self.agentFactory.get_agent(1).draw(self.screen)
            graphics.Graphics.update()

if __name__ == "__main__":
    my_sim = Simulation()
    my_sim.run()
