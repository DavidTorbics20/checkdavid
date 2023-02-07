import tkinter as tk


class CountryObject():
    def __init__(self) -> None:

        L1 = tk.Label(text="Frame 1 Contents")

        L2 = tk.Label(text="Frame 2 Contents")


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Practice with Grid")
    root.geometry("410x380")

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack()

    mylist = tk.Listbox(root, yscrollcommand=scrollbar.set)
    for line in range(100):
        # mylist.insert(END, "This is line number " + str(line))
        item_object = CountryObject()
        mylist.insert(tk.END, item_object)

    mylist.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    scrollbar.config(command=mylist.yview)

    root.mainloop()
