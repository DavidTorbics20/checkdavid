# Import module
from tkinter import *

# Create object
root = Tk()

# Adjust size
root.geometry("200x200")

# Change the label text


def show():
    label.config(text=clicked.get())


# Dropdown menu options
options = [
    "Keys",
    "Barter",
    "Containers",
    "Provisions",
    "Gear",
    "Meds",
    "Sights",
    "Suppressors",
    "Weapon",
    "Ammo",
    "Magazines",
    "Tactical devices",
    "Weapon parts",
    "Special equipment",
    "Maps",
    "Ammo boxes",
    "Currency",
    "Repair"
]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Category")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create button, it will change label text
button = Button(root, text="click Me", command=show)
button.pack()

# Create Label
label = Label(root, text=" ")
label.pack()

# Execute tkinter
root.mainloop()
