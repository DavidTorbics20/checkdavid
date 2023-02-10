"""Main file."""

from gui import GUI


if __name__ == "__main__":
    gui = GUI()
    gui.draw_widgets()
    gui.root.mainloop()
