"""
scorer.py

This class represents a scoreing module to evaluate the fitness of 
a given agent's neural net.

Currently, score is defined as the duration in milliseconds of the pole above
the horizontal with the total distance travelled by the base subtracted off
to encourage minimal effort solutions.
"""

from time import time
from pygame.math import Vector2
import body

class Scorer:
    """Evaluates the fitness of an agent."""

    def __init__(self):
        """Default constructor."""
        self.frames_alive = 0
        self.running = True

        self.__last_pos = None
        self.__total_dist = 0


    def update(self, skeleton):
        """Updates the score.

        Parameters:
        - skeleton (Skeleton): The agent's body definition

        Returns: None
        """

        # only scores while running
        if self.running:
            self.frames_alive += 1

            # Update the total distance traveled by the base
            self.__total_dist += self.__get_dist_moved(skeleton)

            # get the end points of the skeleton
            pt1 = skeleton.points[0]
            pt2 = skeleton.points[1]
            delta = pt2 - pt1

            # scoring should end once pt2 is beneath pt1
            if delta.y >= 0:
                self.running = False


    def __get_dist_moved(self, skeleton):
        """Returns the distance moved since the last recorded position.

        Parameters:
        - skeleton (Skeleton): The skeleton that is being scored.

        Return: (int) Euclidean distance from the last position.
        """

        current_pos = skeleton.points[0]

        # Add a last position if there isn't one
        if self.__last_pos == None:
            self.__last_pos = Vector2(current_pos)
            return 0

        dist = self.__last_pos.distance_to(current_pos)
        self.__last_pos = Vector2(current_pos)
        
        return int(dist)


    def is_done(self):
        """Returns the status of the scorer

        Returns: True if the scorer is no longer running,  False otherwise.
        """
        return not self.running


    def get_score(self):
        """Returns the recorded score calculated as duration - distance travelled.

        Returns: The recorded score (int) so far
        """
        return self.frames_alive - self.__total_dist
