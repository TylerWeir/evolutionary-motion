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

    def __init__(self, num_agents, do_graphics=True):
        """Default constuctor."""
        self.do_graphics = do_graphics
        if do_graphics:
            # Initialize the graphics
            self.screen = graphics.Graphics()
            self.environment = environment.Environment()

        # create list of agents
        self.agents = [agent.Agent() for _ in range(num_agents)]

        


    def run(self):
        """Runs the program."""

        # Function for detecting if a key is pressed down
        if self.do_graphics:
            pressed =  pygame.key.get_pressed()

        while True:
            if self.do_graphics:
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

            if self.do_graphics:
                # Draw the environment again
                self.environment.draw(self.screen)
                # draw agents
                [a.draw(self.screen) for a in self.agents]
                graphics.Graphics.update()
            else:
                # if we're not doing graphics just end the program once the agents are done
                if all([a.scorer.is_done() for a in self.agents]):
                    break
            

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--agents", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of agents to simulate")
    parser.add_argument("-n", "--nographics", action="store_true", help="disable graphics")
    args = parser.parse_args()
    
    if args.agents > 1000:
        if input("Are you sure you want to run the simulation with over 1000 agents? (Y/n) ").lower() != "y":
            exit(0)

    sim = Simulation(args.agents, not args.nographics)
    sim.run()


if __name__ == "__main__":
    main()