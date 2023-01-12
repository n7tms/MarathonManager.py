# Marathon Manager GUI objects
# mmgui.py

# https://www.studytonight.com/tkinter/python-tkinter-geometry-manager
# use a grid() geometry manager
# python tkinter widgets: https://www.studytonight.com/tkinter/python-tkinter-widgets
# Good tutorial/doc: https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html


# import tkinter as tk
from tkinter import Tk, Label, Button

class SitingWindow:
    """The windows used to enter sitings."""
    def __init__(self, master) -> None:
        self.master = master
        master.title("MM4: Sitings")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")   