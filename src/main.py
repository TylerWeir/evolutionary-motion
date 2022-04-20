"""
main.py

This class is used to create an instance of the simulation. 
"""
from curses import KEY_DOWN
import environment
import graphics
import agent
import pygame
from pygame.locals import *

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

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return

            # Draw agent1
            self.agentFactory.get_agent(1).draw(self.screen)
            graphics.Graphics.update()

if __name__ == "__main__":
    my_sim = Simulation()
    my_sim.run()
