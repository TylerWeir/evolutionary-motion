"""
main.py

This class is used to create an instance of the simulation.
"""

import argparse
import pickle
import os

import pygame
from pygame.locals import *
from constants import RANDOM_MIXIN, SCREEN_BACKGROUND_COLOR, SUCCESS_THRESHOLD, MUTATION_DECAY
import environment
import graphics
import agent
import sys
from neural_net import NeuralNet


pygame.init()


class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self, num_agents, do_graphics=True, num_reproducing=1, epochs=10, chain_length=0, **kwargs):
        """Default constuctor."""
        self.do_graphics = do_graphics
        self.num_agents = num_agents
        self.num_reproducing = num_reproducing
        self.chain_length = chain_length
        self.savename = "best_network.net"

        if do_graphics:
            # Initialize the graphics
            self.screen = graphics.Graphics()
            self.environment = environment.Environment()

        # create list of agents
        self.agents = [agent.Agent(chain_length=self.chain_length) for _ in range(num_agents)]

        # Set the active agent
        self.active_agent = 0
        self.set_active_agent(0)

        if kwargs.get("loadfile") is not None:
            self.showcase_loop(kwargs.get("loadfile"))
            exit(0)

        if kwargs.get("savefile") is not None:
            # Save the best network with this name when training is done or the user
            # presses s. Then print a network saved message
            self.savename = kwargs.get("savefile")

        self.mutation_amount = 0.1 # standard deviation in gaussian noise

        self.epochs = epochs
        self.epochs_elapsed = 0

        self.best_agent = None
        self.best_score = -10000000

        self.score_lists = [] # list of lists of scores for each agent on each epoch

        if do_graphics:
            self.font = pygame.font.SysFont("Arial, Times New Roman", 32)
            self.text = self.font.render('Skip endings:', True, (255, 0, 0), SCREEN_BACKGROUND_COLOR)

            self.text_rect = self.text.get_rect()
            self.text_rect.center = (self.screen.get_width() // 2 - 326, self.screen.get_height() // 2 + 240)

            self.epoch_text = self.font.render("Epoch 1", True, (0, 0, 0), SCREEN_BACKGROUND_COLOR)
            self.epoch_text_rect = self.epoch_text.get_rect()
            self.epoch_text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 - 400)

        self.stop_early = True

    def showcase_loop(self, path):
        """Loads the simulation in a display mode for showcaseing a loaded network."""

        if os.path.isdir(path):
            self.agents = []
            for item in os.listdir(path):
                try:
                    net = NeuralNet.net_from_file(os.path.join(path, item))
                    net_input_len = net.input_size
                    a = agent.Agent(net_input_len - 3)
                    a.net = net
                    self.agents.append(a)
                except:
                    pass
            
        elif os.path.isfile(path):
            # Load in the saved network
            display_net = NeuralNet.net_from_file(path)

            # Create an agent with a chain matching the network's input size
            net_input_len = display_net.input_size
            display_agent = agent.Agent(net_input_len-3)
            display_agent.net = display_net

            self.agents = [display_agent]
        
        self.set_active_agent(0)
        
        # Enter the main loop
        while True:
            if self.do_graphics:
                big_cont = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == K_LEFT:
                            self.increment_active_agent(-1)
                        if event.key == K_RIGHT:
                            self.increment_active_agent(1)
                        if event.key == K_r:
                            [a.reset() for a in self.agents]
                            big_cont = True
                            break
                
                if big_cont:
                    continue
            
            alive_agent_count = [a.scorer.is_done() for a in self.agents].count(False)

            if alive_agent_count == 1:
                self.unhighlight_all()

            # update agent
            [a.update(1/60, stop_at_threshold=False) for a in self.agents]

            # Draw the environment again
            if self.do_graphics:
                self.environment.draw(self.screen)

                # draw agents
                [a.draw(self.screen) for a in self.agents if not a.scorer.is_done()]
                if alive_agent_count == 1:
                    [a.net.draw(self.screen) for a in self.agents if not a.scorer.is_done()]
                if self.agents[self.active_agent].scorer.is_done():
                    for i, a in enumerate(self.agents):
                        if not a.scorer.is_done():
                            self.set_active_agent(i)

                graphics.Graphics.update()

            if all(a.scorer.is_done() for a in self.agents):
                [a.reset() for a in self.agents]


    def increment_active_agent(self, direction):
        """Switches the active agent."""
        # Turn off hightlighting on the old agent
        self.agents[self.active_agent].is_highlighted = False
        
        # Change the active agent index
        for _ in self.agents:
            self.active_agent = (self.active_agent + direction) % len(self.agents)
            if self.agents[self.active_agent].scorer.is_done():
                continue
            else:
                break

        # Turn on highlighting for the new active agent
        self.agents[self.active_agent].is_highlighted = True
    

    def unhighlight_all(self):
        for a in self.agents:
            a.is_highlighted = False


    def set_active_agent(self, idx):
        self.unhighlight_all()

        self.active_agent = idx
        self.agents[idx].is_highlighted = True


    def increment_epoch(self):
        """ returns True if the final epoch has elapsed """
        self.mutation_amount *= MUTATION_DECAY

        self.epochs_elapsed += 1
        return self.epochs_elapsed >= self.epochs

        
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
                            self.increment_active_agent(-1)
                        if event.key == K_RIGHT:
                            self.increment_active_agent(1)
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
                    self.increment_active_agent(1)

                # stop early indicator
                self.screen.blit(self.text, self.text_rect)
                self.screen.blit(self.epoch_text, self.epoch_text_rect)
                pygame.draw.rect(self.screen, (0, 255, 0) if self.stop_early else (50, 50, 50), (self.text_rect.right + 10, self.text_rect.top + 5, 30, 30))
                
                graphics.Graphics.update()
            
            # on last epoch, don't stop early
            if self.epochs_elapsed == self.epochs - 1:
                self.stop_early = False

            # if all the agents are done, prepare next generation
            agents_are_done = [a.scorer.is_done() for a in self.agents]
            if all(agents_are_done) or (self.stop_early and agents_are_done.count(False) <= self.num_reproducing):
                # get the best agents
                self.agents.sort(key=lambda x: -x.scorer.get_score())
                best_agents = self.agents[:self.num_reproducing]
                print(f"\nGen {self.epochs_elapsed + 1}/{self.epochs}")
                print("Best scores:", [a.scorer.get_score() for a in best_agents])
                scores = [a.scorer.get_score() for a in self.agents]
                print("Last index of max score:", max(i for i, s in enumerate(scores) if s == self.agents[0].scorer.get_score()))
                print("Average:", sum(scores) / len(scores))

                self.score_lists.append([a.scorer.get_score() for a in self.agents])

                if not self.stop_early:
                    # >= so later successful nets are favored over earlier ones 
                    if best_agents[0].scorer.get_score() >= self.best_score:
                        self.best_score = best_agents[0].scorer.get_score()
                        self.best_agent = best_agents[0]
                    
                # best agents reproduce
                self.agents = [best_agents[i % len(best_agents)].mutated_copy(self.mutation_amount) for i in range(self.num_agents - round(self.num_agents * RANDOM_MIXIN))]
                self.agents += [agent.Agent(chain_length=self.chain_length) for _ in range(round(self.num_agents * RANDOM_MIXIN))]

                self.set_active_agent(0)

                self.epoch_text = self.font.render(f"Epoch {self.epochs_elapsed + 2}", True, (0, 0, 0), SCREEN_BACKGROUND_COLOR)

                if self.increment_epoch():
                    # Sim is over, save the best network and the score stats from training
                    name_with_params = f"{self.savename}_{self.num_agents}a_{self.num_reproducing}r_{self.epochs}e_{SUCCESS_THRESHOLD}"
                    self.best_agent.save_network(name_with_params)
                    with open(f"{name_with_params}_stats.pickle", "wb") as f:
                        pickle.dump(self.score_lists, f)
                    break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--agents", metavar="NUMBER_OF_AGENTS", type=int, default=5, help="number of agents to simulate")
    parser.add_argument("-r", "--reproducers", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of agents that reproduce after each round (must not be greater than the total number of agents)")
    parser.add_argument("-e", "--epochs", metavar="NUMBER_OF_EPOCHS", type=int, default=10, help="number of epochs (rounds of training)")
    parser.add_argument("-c", "--chainlength", metavar="NUMBER_OF_AGENTS", type=int, default=3, help="number of additional segments to add onto the end of the rods")
    parser.add_argument("-n", "--nographics", action="store_true", help="disable graphics")
    parser.add_argument("-l", "--loadname", metavar="NETWORK_NAME", type=str, help="the neural network file to load. Will not train the loaded network")
    parser.add_argument("-s", "--savename", metavar="NETWORK_NAME", type=str, help="the name of the file the best network will be saved in")
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

    sim = Simulation(args.agents, not args.nographics, num_reproducing=args.reproducers, epochs=args.epochs, chain_length=chain_length, loadfile=args.loadname, savefile=args.savename)
    sim.run()

if __name__ == "__main__":
    main()
