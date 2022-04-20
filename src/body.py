"""
body.py

Uses points and sticks to define skeletons for the agent's 
in the simulated environment.
"""

import pygame
from pygame.math import Vector2

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
            #TODO: Here is where to apply acceleration
            acceleration = (0, 100)
            current_pos = Vector2(point) # Avoids alias issues
            old_pos = self.old_points[i]

            self.points[i] = current_pos - old_pos + acceleration*delta_t**2
            old_pos.update(current_pos)

        # After moving the points, satisfy the constraints
        self.satisfy_constriants()

    def satisfy_constriants(self):
        """Satisfys bounds and stick constraints between points.

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
                pos_1 += delta*0.5*diff
                pos_2 -= delta*0.5*diff

    def draw(self, canvas):
        """Draws the skeleton.

        Parameters:
        - canvas: The pygame canvas to draw on.

        Returns: None
        """
        pass
