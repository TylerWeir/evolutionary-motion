"""
graphics.py

Contains a singleton Graphics class used to manage the window and rendering
of the simulation.
"""

from re import I
import tkinter as tk

class Graphics(tk.Tk):
    """Manages the graphics of the simulation."""

    __window = None

    def __new__(cls, *args):
        if cls.__window is None:
            cls.__window = super().__new__(cls, *args)
        return cls.__window

    def display_message(self, message):
        label = tk.Label(self.__window, text=message) # Display the message in the window
        label.pack(padx=20, pady=20)

    def render_window(self):
        """Starts the tkinter objects mainloop."""
        #TODO: This is a blocking operation, not sure what to do,
        # maybe make a thread to run the loop? or just call last
        self.__window.mainloop()

if __name__ == "__main__":
    window = Graphics()
    window.display_message("Hello World")
    window.render_window()