#!/usr/bin/python
from Tkinter import *
from ttk import *
from window_class import Window

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
if __name__ == "__main__":
    root = Tk()
    #size of the window
    root.geometry("1300x750")

    app = Window(root)
    root.mainloop()  