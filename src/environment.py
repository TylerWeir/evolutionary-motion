"""
environment.py

This is the simulated world in which the agents exist. Currently
The world is empty space in which agents move horizontally attempting
to balance a pole.
"""
import pygame

from constants import TRACK_WIDTH, AGENT_BASE_HEIGHT, AGENT_BASE_WIDTH


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
        surface.fill((255, 255, 255))

        # draw track
        pygame.draw.rect(surface, (0, 0, 0), (surface.get_width() / 2 - TRACK_WIDTH / 2 - AGENT_BASE_WIDTH / 2, surface.get_height() * 2 / 3 + AGENT_BASE_HEIGHT / 2, TRACK_WIDTH + AGENT_BASE_WIDTH, AGENT_BASE_HEIGHT / 2))

