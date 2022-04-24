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
        self.agent = agent.Agent()

        self.environment = environment.Environment()

    def run(self):
        """Runs the program."""

        # Function for detecting if a key is pressed down
        pressed =  pygame.key.get_pressed()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == K_LEFT:
                        self.agent.move(-1)
                    if event.key == K_RIGHT:
                        self.agent.move(1)

            # Update agent1
            self.agent.update(1/60)

            # Draw the environment again
            self.environment.draw(self.screen)

            # Draw agent1
            self.agent.draw(self.screen)
            graphics.Graphics.update()

if __name__ == "__main__":
    my_sim = Simulation()
    my_sim.run()
