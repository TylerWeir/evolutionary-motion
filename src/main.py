"""
main.py

This class is used to create an instance of the simulation.
"""

import argparse

import pygame
from pygame.locals import *
from constants import SCREEN_BACKGROUND_COLOR
import environment
import graphics
import agent
import sys
from neural_net import NeuralNet


pygame.init()

class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self, num_agents, do_graphics=True, num_reproducing=1, chain_length=0, **kwargs):
        """Default constuctor."""
        self.do_graphics = do_graphics
        self.num_agents = num_agents
        self.num_reproducing = num_reproducing
        self.savename = "best_network.net"

        if do_graphics:
            # Initialize the graphics
            self.screen = graphics.Graphics()
            self.environment = environment.Environment()

        if kwargs.get("loadfile") is not None:
            # TODO dont train and just load then display the network on a loop
            self.showcase_loop(kwargs.get("loadfile"))

        if kwargs.get("savefile") is not None:
            # Save the best network with this name when training is done or the user
            # presses s. Then print a network saved message
            self.savename = kwargs.get("savefile")

        # create list of agents
        self.agents = [agent.Agent(chain_length=chain_length) for _ in range(num_agents)]

        self.mutation_amount = 0.1 # standard deviation in gaussian noise
        self.mutation_decay = 0.98

        self.epochs = 50
        self.epochs_elapsed = 0

        self.best_agent = None
        self.best_score = -10000000

        # Set the active agent
        self.active_agent = 0
        self.switch_active_agent(0)

        if do_graphics:
            self.font = pygame.font.SysFont("Arial, Times New Roman", 32)
            self.text = self.font.render('Skip endings:', True, (255, 0, 0), SCREEN_BACKGROUND_COLOR)

            self.text_rect = self.text.get_rect()
            self.text_rect.center = (self.screen.get_width() // 2 - 500, self.screen.get_height() // 2)

        self.stop_early = True and do_graphics

    def showcase_loop(self, filename):
        """Loads the simulation in a display mode for showcaseing a loaded network."""

        # Load in the saved network
        display_net = NeuralNet.net_from_file(filename)

        # Create an agent with a chain matching the network's input size
        net_input_len = display_net.input_size
        display_agent = agent.Agent(net_input_len-3)
        
        # Enter the main loop
        while True:
            if self.do_graphics:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            # update agent
            display_agent.update(1/60)

            # Draw the environment again
            self.environment.draw(self.screen)

            # draw the agent and its network
            display_agent.draw(self.screen)
            display_agent.net.draw(self.screen)
            graphics.Graphics.update()

            # if the agent falls over, reset it
            if display_agent.scorer.is_done():
                display_agent.reset()


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


    def increment_epoch(self):
        """ returns True if the final epoch has elapsed """
        self.mutation_amount *= self.mutation_decay

        self.epochs_elapsed += 1
        if self.epochs_elapsed >= self.epochs:
            return True

        
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
                        if event.key == K_SPACE:
                            self.stop_early = not self.stop_early
                        
                        if event.key == K_p:
                            print(self.agents[self.active_agent].nn_weights_string())

                        if event.key == K_s:
                            print(self.agents[self.active_agent].scorer.get_score())

                        if event.key == K_n:
                            print(f"Saved the network \`{self.savename}\`")
                            self.agents[self.active_agent].save_network(self.savename)
                            sys.exit()

            # update agents
            [a.update(1/60) for a in self.agents]

            if self.do_graphics:
                # Draw the environment again
                self.environment.draw(self.screen)
                # draw agents
                [a.draw(self.screen) for a in self.agents if not a.scorer.is_done()]
                if self.agents[self.active_agent].scorer.is_done():
                    for i, a in enumerate(self.agents):
                        if not a.scorer.is_done():
                            self.switch_active_agent(i)
                self.screen.blit(self.text, self.text_rect)

                pygame.draw.rect(self.screen, (0, 255, 0) if self.stop_early else (50, 50, 50), (self.text_rect.right + 10, self.text_rect.top, 30, 30))
                
                graphics.Graphics.update()

            # if all the agents are done, prepare next generation
            agents_are_done = [a.scorer.is_done() for a in self.agents]
            if all(agents_are_done) or (self.stop_early and agents_are_done.count(False) <= self.num_reproducing):
                # find best agent by index of False in scores
                if self.stop_early:
                    best_agents = [a for a in self.agents if not a.scorer.is_done()]
                    self.agents = [best_agents[i % len(best_agents)].mutated_copy(self.mutation_amount) for i in range(self.num_agents)]
                else:
                    best_score = -10000000
                    best_agent = None
                    for a in self.agents:
                        if a.scorer.get_score() > best_score:
                            best_score = a.scorer.get_score()
                            best_agent = a
                    
                    self.agents = [best_agent.mutated_copy(self.mutation_amount) for _ in range(self.num_agents)]
                    
                    print(f"Best score from generation {self.epochs_elapsed}: {best_agent.scorer.get_score()}")
                    
                    if best_agent.scorer.get_score() > self.best_score:
                        self.best_score = best_agent.scorer.get_score()
                        self.best_agent = best_agent.copy()
                        print("New best agent network: ")
                        print(self.best_agent.net)

                self.switch_active_agent(0)
                if self.increment_epoch(): 
                    # Sim is over, save the best network
                    self.best_agent.save_network(self.savename)
                    break
            

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--agents", metavar="NUMBER_OF_AGENTS", type=int, default=5, help="number of agents to simulate")
    parser.add_argument("-r", "--reproducers", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of agents that reproduce after each round (must not be greater than the total number of agents)")
    parser.add_argument("-c", "--chainlength", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of additional segments to add onto the end of the rods")
    parser.add_argument("-n", "--nographics", action="store_true", help="disable graphics")
    parser.add_argument("-l", "--loadname", metavar="NETWORK_NAME", type=str, help="the neural network file to load. Will not train the loaded network")
    parser.add_argument("-s", "--savename", metavar="NETWORK_NAME", type=str, help="the name of the file the network will be saved in")
    args = parser.parse_args()
    
    if args.agents > 1000:
        if input("Are you sure you want to run the simulation with over 1000 agents? (Y/n) ").lower() != "y":
            exit(0)

    if args.reproducers > args.agents:
        print("There cannot be more reproducers than total agents.")
        exit(0)

    # Make load and save mutually exclusive
    if args.loadname != None and args.savename != None:
        print("[main]: load and save are mutually exclusive")
        sys.exit()

    chain_length = args.chainlength if args.chainlength is not None else 0

    sim = Simulation(args.agents, not args.nographics, num_reproducing=args.reproducers, chain_length=chain_length, loadfile=args.loadname, savefile=args.savename)
    sim.run()

if __name__ == "__main__":
    main()
