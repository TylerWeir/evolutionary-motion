"""
main.py

This class is used to create an instance of the simulation. 
"""

from re import I
import environment
import graphics

class Simulation:
    """Creates a simulated environment containing ANN controlled agents."""

    def __init__(self):
        """Default constuctor."""

        # Initialize the graphics
        window = graphics.Graphics()
        window.display_message("Hello World")
        window.render_window() #TODO: This is blocking...
        
if __name__ == "__main__":
    my_sim = Simulation()