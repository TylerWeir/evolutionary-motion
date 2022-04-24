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
        self.start_time = None
        self.end_time = None
        self.running = False

        self.__last_pos = None
        self.__total_dist = 0

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

            # Update the total distance traveled by the base
            self.__total_dist += self.__get_dist_moved(skeleton)

            # get the end points of the skeleton
            pt1 = skeleton.points[0]
            pt2 = skeleton.points[1]
            delta = pt2 - pt1

            # scoring should end once pt2 is beneath pt1
            if delta.y >= 0:
                self.end_time = int(time() * 1000) # Milliseconds
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

        Returns: True if the scorer is actively running, False otherwise.
        """
        if self.start_time != None and self.end_time != None and not self.running:
            return True
        return False


    def get_score(self):
        """Returns the recorded score calculated as duration - distance travelled.

        Returns: The recorded score (int) or -1 if the score is not yet available.
        """

        if not self.is_done():
            return -1

        duration = self.end_time - self.start_time

        # subtract total distance to penalize the agent for moving around too much
        score = duration - self.__total_dist

        return score
