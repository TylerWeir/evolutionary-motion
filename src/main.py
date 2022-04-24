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


NUM_AGENTS = 10


class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self):
        """Default constuctor."""
        # Initialize the graphics
        self.screen = graphics.Graphics()

        # create list of agents
        self.agents = [agent.Agent() for _ in range(NUM_AGENTS)]

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
                    
                    if event.key == K_p:
                        print(self.agent.nn_weights_string())

            # update agents
            [a.update(1/60) for a in self.agents]

            # Draw the environment again
            self.environment.draw(self.screen)

            # draw agents
            [a.draw(self.screen) for a in self.agents]
            
            graphics.Graphics.update()


if __name__ == "__main__":
    my_sim = Simulation()
    my_sim.run()
