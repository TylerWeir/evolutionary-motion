"""
environment.py

This is the simulated world in which the agents exist. Currently
The world is empty space in which agents move horizontally attempting
to balance a pole.
"""
import pygame

class Environment:

    def __init__(self):
        """Default constructor."""
        pass


    def draw(self, surface):
        """Draws the environment to the given canvas.

        Parameters:
        - surface (pygame.Surface): A pygame surface to draw on.

        Returns: None
        """
        surface.fill((232, 232, 232))


