"""
main.py

This class is used to create an instance of the simulation.
"""

import argparse

import pygame
from pygame.locals import *

import environment
import graphics
import agent


class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self, num_agents, do_graphics=True):
        """Default constuctor."""
        self.do_graphics = do_graphics
        self.num_agents = num_agents
        if do_graphics:
            # Initialize the graphics
            self.screen = graphics.Graphics()
            self.environment = environment.Environment()

        # create list of agents
        self.agents = [agent.Agent() for _ in range(num_agents)]

        self.mutation_amount = 1 # standard deviation in gaussian noise
        self.mutation_decay = 0.98

        self.epochs = 50
        self.epochs_elapsed = 0

        self.best_agent = None
        self.best_score = -10000000

        # Set the active agent
        self.active_agent = 0
        self.switch_active_agent(0)

    def switch_active_agent(self, direction):
        """Switches the active agent."""
        # Turn off hightlighting on the old agent
        self.agents[self.active_agent].is_highlighted = False
        
        # Change the active agent index
        self.active_agent += direction
        if self.active_agent < 0:
            self.active_agent = len(self.agents)-1
        if self.active_agent >= len(self.agents):
            self.active_agent = 0

        # Turn on highlighting for the new active agent
        self.agents[self.active_agent].is_highlighted = True


        
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
                            self.switch_active_agent(-1)
                        if event.key == K_RIGHT:
                            self.switch_active_agent(1)
                        
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

            # if all the agents are done, prepare next generation
            if all([a.scorer.is_done() for a in self.agents]):
                scored_agents = [(a.get_score(), a) for a in self.agents]
                scored_agents.sort()
                self.agents = [scored_agents[-1][1].mutated_copy(self.mutation_amount) for _ in range(self.num_agents)]
                
                best_this_gen = scored_agents[-1][0]

                print(f"Best score from generation {self.epochs_elapsed}: {best_this_gen}")

                self.mutation_amount *= self.mutation_decay

                if best_this_gen > self.best_score:
                    self.best_score = best_this_gen
                    self.best_agent = scored_agents[-1][1].copy()
                    print("New best agent network: ")
                    print(self.best_agent.net)

                self.epochs_elapsed += 1
                if self.epochs_elapsed >= self.epochs:
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
