"""
graphics.py

Contains a singleton Graphics class used to manage the window and rendering
of the simulation.
"""

import pygame

class Graphics():
    """Manages the graphics of the simulation."""

    __window = None

    def __new__(cls, *args):
        """Creates the singleton instance of the graphics.

        Returns: The singleton instance of the graphics.
        """
        if cls.__window is None:
            # Initialize pygame
            cls.__window = pygame.display.set_mode(*args)
            cls.__window.fill((232, 232, 232))
        return cls.__window

    @staticmethod
    def update():
        """Updates the display

        Returns: None"""
        pygame.display.update()

if __name__ == "__main__":
    window = Graphics()

    pygame.draw.circle(window, (255, 255, 255), (20, 20), 20, 0)

    while True:
        Graphics.update()
