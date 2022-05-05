"""
agent.py

Reprsents an agent operating in the simulated environment. Each agent contains a 
unique instance of an evolutionary neural network to control its movements.

Large amounts of state will be kept in the objects such as positions, orientations, 
velocities.

"""
import abc
import random
from math import atan2, cos, sin

import pygame
from pygame.math import Vector2

from body import Skeleton
from neural_net import NeuralNet
from activations import *
from scorer import Scorer
from environment import TRACK_WIDTH
from constants import *


class Agent():
    """Agent defines a pole balancing entity. Each agent is made
    up a scoring object, a neural net, and a skeleton."""

    def __init__(self, chain_length=0):
        """Default constructor. Defines an agent with a random 
        neural net.

        Returns: None
        """

        # set argument properties
        if type(chain_length) != int:
            raise Exception("property chain_length must be an int")

        self.chain_length = chain_length

        # An abstract position which is later
        # mapped to the center of the screen as zero.
        self.pos = Vector2((0,0))
        self.vel = Vector2((0,0))

        self.move_strength = 1.5 # how strong the force is when the player tries to move

        # Define the skeleton backing the agent
        points = [(0, 0), (1, -260)] + [(1, -300 - i*40) for i in range(chain_length)]
        sticks = [(i, i+1) for i, _ in enumerate(points[:-1])]
        self.skeleton = Skeleton(points, sticks)

        # Used to show which agent is selected
        self.is_highlighted = False

        # Define a score keeper for the agent
        self.scorer = Scorer()

        # Define a NeuralNet for the agent
        # input layer is base position, base velocity, x position relative to base for all other ponts
        self.net = NeuralNet(len(points) + 1, 1, tanh)
        self.net.add_hidden_layer(6, tanh)
        self.net.add_hidden_layer(6, tanh)
        self.net.add_hidden_layer(3, tanh)

        self.base_color = tuple([random.randint(40, 120) for _ in range(3)])
        self.rod_color = tuple([random.randint(100, 180) for _ in range(3)])


    def move(self, x):
        """Moves the agent by the indicated amount on the x axis

        Parameters:
        - x (number): The horizontal distance to move

        Returns: None
        """

        # move the base
        self.pos.x = max(min(self.pos.x + x, TRACK_WIDTH / 2), -TRACK_WIDTH / 2)

        # make the skeleton base match the agent
        self.skeleton.force_pos(0, self.pos)

    
    def apply_force(self, x_force, delta_t):
        """Applies a force to the agent

        Parameters:
        - x_force (number): The force to move the agent with along the x-axis (can be negative)

        Returns: None
        """

        net_force = x_force + random.uniform(-BASE_FORCE_NOISE, BASE_FORCE_NOISE) # add some noise to the force

        self.vel.x += net_force * self.move_strength * delta_t
        # friction would go here though I think that's handled elsewhere
        self.move(self.vel.x)


    def update(self, delta_t):
        """Updates the agent given the time step.

        Parameters:
        - delta_t (float): The number of seconds that have passed since
                           the last frame.
        """

        # only update if the pole is airborne
        if not self.scorer.is_done():
            # get the direction of effort
            point_positions = [self.skeleton.points[i+1][0] - self.skeleton.points[i][0] for i in range(self.chain_length + 1)]
            effort_vector = self.net.evaluate(np.array([self.vel.x, self.pos.x] + point_positions))
            move_force = tanh(effort_vector[0])
            # print(f"{rod_tip_pos_relative_to_base=} {effort_vector=} {move_force=}")
            self.apply_force(move_force, delta_t)
            self.skeleton.move(delta_t)
            self.scorer.update(self.skeleton)


    def nn_weights_string(self):
        return str(self.net)


    def get_score(self):
        return self.scorer.get_score()

    
    def new_copy(self, preserve_color=False):
        a = Agent(self.chain_length)
        a.net = self.net.copy()
        if preserve_color:
            a.base_color = self.base_color
            a.rod_color = self.rod_color
        
        return a
    

    def mutated_copy(self, mutation_amount=1, preserve_color=False):
        a = Agent(self.chain_length)
        a.net = self.net.noisy_copy(std_dev=mutation_amount)
        if preserve_color:
            a.base_color = self.base_color
            a.rod_color = self.rod_color
        
        return a


    def copy(self, preserve_color=False):
        a = self.new_copy(preserve_color=preserve_color)
        a.pos = Vector2(self.pos)
        a.vel = Vector2(self.vel)

        return a

    def __highlight(self, canvas):
        width = canvas.get_width()
        height = canvas.get_height()

        glowing_base_pos = (
            self.pos.x + width/2 - 20 - 4,
            self.pos.y + height*2/3 - 10 - 4,
            AGENT_BASE_WIDTH+8,
            AGENT_BASE_HEIGHT+4,
        )

        myRect = pygame.Rect((glowing_base_pos))
        self.draw_glowing_rect(canvas, (255,0,0), myRect)

        self.__draw_glowing_pole(canvas)


    def __draw_glowing_pole(self, canvas):

        # get the end points of the skeleton
        pt1 = self.skeleton.points[0]
        pt2 = self.skeleton.points[1]
        delta = pt2 - pt1

        length = pt1.distance_to(pt2) + HIGHLIGHT_THICKNESS
        radius = AGENT_POLE_RADIUS + HIGHLIGHT_THICKNESS

        width = canvas.get_width()
        height = canvas.get_height()
        base_pos = (self.pos.x + width/2, self.pos.y + height*2/3, 40, 20)
        
        # Find the angle of rotation
        rads = atan2(delta.y, delta.x)
       
        # This is how new points are calculated 
        # new_x_point = old_x_point * cos(Angle) - old_y_point * sin(Angle);
        # new_y_point = old_y_point * cos(Angle) + old_x_point * sin(Angle);
        sin_rads = sin(rads)
        cos_rads = cos(rads)

        x1 = radius * sin_rads
        x2 = -radius * sin_rads
        x3 = length * cos_rads - radius * sin_rads
        x4 = length * cos_rads + radius * sin_rads
        
        y1 = -radius * cos_rads
        y2 = radius * cos_rads
        y3 = radius * cos_rads + length * sin_rads
        y4 = -radius * cos_rads + length * sin_rads

        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        # map the offset through the points
        points = [(x + base_pos[0], y + base_pos[1]) for (x, y) in points]
        self.draw_glowing_polygon(canvas, (255, 0, 0), points)


    def draw_glowing_rect(self, surface, color, rect):
        # Draw the glowing pole and glowing base first
        base_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        base_surf.set_alpha(HIGHLIGHT_ALPHA)
        pygame.draw.rect(base_surf, (255, 0, 0), base_surf.get_rect())
        surface.blit(base_surf, rect)


    def draw_glowing_polygon(self, surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        shape_surf.set_alpha(HIGHLIGHT_ALPHA)
        pygame.draw.polygon(shape_surf, color, [(x-min_x, y-min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)


    def __draw_pole(self, canvas):

        for stick in self.skeleton.sticks:

            # get the end points of the skeleton
            pt1 = self.skeleton.points[stick[0]]
            pt2 = self.skeleton.points[stick[1]]
            delta = pt2 - pt1

            radius = AGENT_POLE_RADIUS
            length = pt1.distance_to(pt2)

            width = canvas.get_width()
            height = canvas.get_height()
            base_pos = (pt1.x + width/2, pt1.y + height*2/3, 40, 20)

            # Find the angle of rotation
            rads = atan2(delta.y, delta.x)
           
            # This is how new points are calculated 
            # new_x_point = old_x_point * cos(Angle) - old_y_point * sin(Angle);
            # new_y_point = old_y_point * cos(Angle) + old_x_point * sin(Angle);
            sin_rads = sin(rads)
            cos_rads = cos(rads)

            x1 = radius * sin_rads
            x2 = -radius * sin_rads
            x3 = length * cos_rads - radius * sin_rads
            x4 = length * cos_rads + radius * sin_rads
            
            y1 = -radius * cos_rads
            y2 = radius * cos_rads
            y3 = radius * cos_rads + length * sin_rads
            y4 = -radius * cos_rads + length * sin_rads

            points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

            # map the offset through the points
            points = [(x + base_pos[0], y + base_pos[1]) for (x, y) in points]
            
            # pygame.draw.polygon(canvas, (226, 41, 55), points)
            pygame.draw.polygon(canvas, self.rod_color, points)


    def draw(self, canvas):
        """Draws the agent to the given canvas.

        Parameters:
        - canvas (pygame.surface): A pygame surface to draw onto.

        Returns: None
        """

        if self.is_highlighted:
           self.__highlight(canvas)
           self.net.draw(canvas)

        # Draw relative to window size
        width = canvas.get_width()
        height = canvas.get_height()

        base_pos = (
            self.pos.x + width/2 - 20,
            self.pos.y + height*2/3 - 10,
            AGENT_BASE_WIDTH,
            AGENT_BASE_HEIGHT
        )
        pygame.draw.rect(canvas, self.base_color, base_pos, 0)

        self.__draw_pole(canvas)

        # For now also draw the skeleton
        # self.skeleton.draw(canvas)

    def __lt__(self, other):
        return True
