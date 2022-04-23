"""
scorer.py

This class represents a scoreing module to evaluate the fitness of 
a given agent's neural net.

Currently, score is defined as miliseconds of the pole above horizontal.
"""

from time import time
from pygame.math import Vector2
import body

class Scorer:
    """Evaluates the fitness of an agent."""

    def __init__(self):
        """Default constructor."""
        self.start_time = None
        self.end_time = None
        self.running = False

    def start(self):
        """Begins the scoring period.

        Returns: None
        """
        # Convert time to milliseconds
        self.start_time = int(time()*1000)
        self.running = True

    def update(self, skeleton):
        """Updates the score.

        Parameters:
        - body (Body): The agent's body definition

        Returns: None
        """
        # Starts scoring if not already
        if self.start_time == None:
            self.start()

        # only scores while running
        if self.running:
            # get the end points of the skeleton
            pt1 = skeleton.points[0]
            pt2 = skeleton.points[1]
            delta = pt2 - pt1

            # scoring should end once pt2 is beneath pt1
            if delta.y >= 0:
                self.end_time = int(time() * 1000) # Milliseconds
                self.running = False

    def is_done(self):
        """Returns the status of the scorer

        Returns: True if the scorer is actively running, False otherwise.
        """
        if self.start_time != None and self.end_time != None and not self.running:
            return True
        return False

    def get_score(self):
        """Returns the recorded score.

        Returns: The recorded score (int) or -1 if the score is not yet available.
        """

        if not self.is_done():
            return -1

        return self.end_time - self.start_time
