"""
main.py

This class is used to create an instance of the simulation.
"""

import sys
import argparse
from curses import KEY_DOWN

from pygame.locals import *

import environment
import graphics
import agent
import pygame


class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self, num_agents):
        """Default constuctor."""
        # Initialize the graphics
        self.screen = graphics.Graphics()

        # create list of agents
        self.agents = [agent.Agent() for _ in range(num_agents)]

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--numagents", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of agents to simulate")
    args = parser.parse_args()
    
    if args.numagents >= 1000:
        if input("Are you sure you want to run the simulation with over 1000 agents? (Y/n) ").lower() != "y":
            exit(0)

    sim = Simulation(args.numagents)
    sim.run()


if __name__ == "__main__":
    main()