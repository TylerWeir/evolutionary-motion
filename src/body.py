"""
body.py

Uses points and sticks to define skeletons for the agent's 
in the simulated environment.
"""

import random

import pygame
from pygame.math import Vector2

import graphics
from constants import *

class Skeleton:
    """Represents a rigid body structure and it's constraints."""

    def __init__(self, points, sticks, old_points=None):
        """Creates a new Skeleton from a list of points.

        Parameters:
        - points [(x, y)]: A list of points defining the skeleton shape.
        - sticks [(p1, p2)]: A list of points to connect via a stick.

        kwargs:
        - old_points=None [(x, y)]: Used to give points an initial velocity.

        Returns: None
        """
        # Convert all the points to Vectors for easy maniputlation
        self.points = [Vector2(p) for p in points]

        # If no old points are specified, the object should start at rest
        if old_points == None:
            self.old_points = [Vector2(p) for p in points]
        else:
            self.old_points = [Vector2(p) for p in old_points]

        self.locked_points = []

        # Sticks are defined as (p1, p2, distance)
        self.sticks = [(a, b, self.points[a].distance_to(self.points[b])) for (a, b) in sticks]


    def move(self, delta_t):
        """Verlet Integration step.

        Parameters:
        - delta_t (float): The amount of time to step forward.

        Returns: None
        """
        # Iterate through the points and move them according to the Verlet
        # integration routine.
        for i, point in enumerate(self.points):
            if i not in self.locked_points:
                acc_noise = random.uniform(-ROD_ACC_NOISE, ROD_ACC_NOISE)
                acceleration = Vector2((0 + acc_noise, 100 + acc_noise))
                current_pos = Vector2(point) # Avoids alias issues
                old_pos = self.old_points[i]

                self.points[i] += (current_pos - old_pos)*0.999 + acceleration*delta_t**2
                old_pos.update(current_pos)

        # After moving the points, satisfy the constraints
        self.satisfy_constraints()


    def satisfy_constraints(self):
        """Satisfies bounds and stick constraints between points.

        Returns: None
        """
        # Number of iterations to satisfy constraints
        for _ in range(3):
            #TODO Other worldly constraints go here

            for stick in self.sticks:
                # Get the points
                pos_1 = self.points[stick[0]]
                pos_2 = self.points[stick[1]]

                # Vector between the points
                delta = pos_2 - pos_1
                len_delta =  delta.length()
                diff = (len_delta-stick[2])/len_delta

                # Update the points position according to difference
                # from the constraint distance
                if stick[0] not in self.locked_points:
                    pos_1 += delta*0.5*diff
                if stick[1] not in self.locked_points:
                    pos_2 -= delta*0.5*diff


    def force_pos(self, point_index, position : Vector2):
        """Forces a point to a given position.

        Parameters:
        - point_index (int): The point to force to a position.
        - position (x, y): The position to force the point to.

        Returns: None
        """
        # If the point is not already locked then lock it.
        if self.locked_points.count(point_index) == 0:
            self.locked_points.append(point_index)

        # Move the point to the new position
        self.points[point_index] = position


    def free_point(self, point_index):
        # Remove the point from the locked points list
        self.locked_points.remove(point_index)

        # Set the point velocity to zero to avoid jumping from
        # the original pre-locking position
        self.old_points[point_index].x = self.points[point_index].x
        self.old_points[point_index].y = self.points[point_index].y


    def draw(self, canvas):
        """Draws the skeleton.

        Parameters:
        - canvas: The pygame canvas to draw on.

        Returns: None
        """

        # Set the zero to the middle of the screen
        # two thirds of the way down
        zero_x = canvas.get_width()/2
        zero_y = canvas.get_height()*2/3
        zero = Vector2(zero_x, zero_y)

        # Draw the points
        for _, point in enumerate(self.points):
            pygame.draw.circle(canvas, (0, 255, 0), zero+point, 4)

        # Draw the sticks
        for stick in self.sticks:
            # End points of the stick
            pt1 = zero + self.points[stick[0]]
            pt2 = zero + self.points[stick[1]]

            pygame.draw.line(canvas, (0, 255, 0), pt1, pt2)


