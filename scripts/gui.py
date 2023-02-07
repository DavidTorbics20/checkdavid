"""GUI overlay for the application."""

import tkinter as tk
from tkinter import ttk
from table_management import TableManagement as TM
import threading


class GUI():
    def __init__(self):
        self.root = tk.Tk()
        # self.root = ThemedTk(theme="arc")
        self.root.geometry("1080x800+450+150")
        self.root.title("CheckDavid")
        self.root.resizable(0, 0)

        self.root.columnconfigure((0), weight=1)
        self.root.columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=2)
        self.root.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                10, 11, 12, 13, 14, 15, 16), weight=0)

        self.clicked = tk.StringVar(self.root)

        self.options = [
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

        self.starting_pos = 0

    def show_category(self):
        category = self.clicked.get()
        self.category_label.config(text=self.clicked.get())
        return category

    def draw_widgets(self):
        input_text = ""

        # Input field
        username_label = ttk.Entry(self.root, textvariable=input_text, font=("", 24))
        username_label.grid(column=0, row=0, columnspan=4, sticky=tk.EW, padx=60, pady=5)

        # Dropdown menu for to choose the category
        self.clicked.set("Category")
        drop_menu = tk.OptionMenu(self.root, self.clicked, *self.options)
        drop_menu.configure(width=15, height=3)
        drop_menu.grid(column=4, row=0, sticky=tk.EW, padx=5, pady=5)
        self.category_label = ttk.Label(self.root, text=" ")

        # self.clicked.trace('w', self.change_shown_category)

        search_btn = tk.Button(self.root, text="Search", command=self.change_shown_category,
                               width=15, height=3)
        search_btn.grid(column=5, row=0, sticky=tk.W, padx=5, pady=5)

        # Start search with selected Category
        # If no categry is selected the default page will be loaded
        update_btn = tk.Button(self.root, text="Update", command=self.update_btn_function,
                               width=15, height=3)
        update_btn.grid(column=6, row=0, sticky=tk.W, padx=5, pady=5)

        # Show bookmarked items
        tk_image = tk.PhotoImage(file=r'C:\\Users\\torbi\\source\\repos\\SchoolRepos\\' +
                                 '2022-2023\\INSY-SEW\\checkdavid\\' +
                                 'media\\bookmark-icon2.png')
        bookmark_btn = tk.Button(self.root, text="aaa", image=tk_image, width=50, height=50)
        bookmark_btn.image = tk_image
        bookmark_btn.grid(column=7, row=0, sticky=tk.W, padx=5, pady=5)

        # The Label for the current page counter
        item_name = tk.Label(self.root, text="(Items XX to YY) out of (ZZ Total)",
                             background='pink')
        item_name.grid(column=3, row=2, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # The buttons to cycle the the category left and right
        next_page_btn = tk.Button(self.root, text="Next page", command=self.change_shown_category,
                                  width=15, height=3)
        next_page_btn.grid(column=5, row=2, sticky=tk.W, padx=5, pady=5)
        previouse_page_btn = tk.Button(self.root, text="Previouse page",
                                       command=self.get_previous_items,
                                       width=15, height=3)
        previouse_page_btn.grid(column=2, row=2, sticky=tk.E, padx=5, pady=5)

        # The row with the page scroll buttons

    def show_items_from_db(self, current_values):
        # Temporarily the image is the same for every item
        tk_image = tk.PhotoImage(file=r'C:\\Users\\torbi\\source\\repos\\SchoolRepos\\' +
                                      '2022-2023\\INSY-SEW\\checkdavid\\' +
                                      'media\\12.7x55_mm_ps12_sm.png')
        tk_image.image = tk_image

        name = "name"
        price = "price"
        pps = "pps"
        change = "change"
        trader_name = "t_n"
        trader_price = "t_p"

        # get item with the according to the current i value + the page counter min
        for i, item in enumerate(current_values):

            i = i + 1

            try:
                search_btn = tk.Label(self.root, text="Image", background='gray79', image=tk_image)
                search_btn.grid(column=2, row=1 + 2 * i + (i - 1), rowspan=3, sticky=tk.NSEW,
                                padx=5, pady=5)

                item_name = tk.Label(self.root, text=name, font=("", 14), background='red')
                item_name.grid(column=3, row=1 + 2 * i + (i - 1), columnspan=3, sticky=tk.NSEW,
                               padx=2, pady=5)
                item_name.config(text=item.item_name)

                item_name = tk.Label(self.root, text=price,
                                     font=("", 10), background='green')
                item_name.grid(column=3, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)
                item_name.config(text=item.price)

                item_name = tk.Label(self.root, text=pps,
                                     font=("", 10), background='light blue')
                item_name.grid(column=4, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)
                item_name.config(text=item.price_per_slot)

                item_name = tk.Label(self.root, text=change,
                                     font=("", 10), background='yellow')
                item_name.grid(column=5, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)
                item_name.config(text=str(item.h_change + " / " + item.d_change))

                item_name = tk.Label(self.root, text=trader_name,
                                     font=("", 10), background='yellow')
                item_name.grid(column=3, row=3 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)
                item_name.config(text=item.trader_price)

                item_name = tk.Label(self.root, text=trader_price,
                                     font=("", 10), background='yellow')
                item_name.grid(column=4, row=3 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)
                item_name.config(text=item.trader_name)
            except Exception:
                print("hmmm...something went wrong")

    def refresh_selection(self):
        """
        Thie function is called when every minute.
        It searched for the items in a specific category
        and displays them afterwards."""

    def check_if_still_downloading(self):
        self.table_manager = TM(self.show_category())
        downloader_task = threading.Thread(target=self.table_manager.search_for_items)
        downloader_task.start()

        while True:
            if not downloader_task.is_alive():
                current_page_values = self.table_manager.get_current_page_values()
                self.show_items_from_db(current_page_values)
                break

    def update_btn_function(self):
        checking_task = threading.Thread(target=self.check_if_still_downloading)
        print(self.show_category())
        checking_task.start()

    def get_next_items(self):
        # basically do this
        # self.current_page_values = table_manager.get_current_page_values()

        # or just do start_pos += 7
        self.starting_pos += 7
        current_page_values = self.table_manager.get_current_page_values()
        self.show_items_from_db(current_page_values)

    def get_previous_items(self):
        # basically do this
        # self.current_page_values = table_manager.get_current_page_values()

        # or just do start_pos -= 7
        self.starting_pos -= 7
        if self.starting_pos < 1:
            self.starting_pos = 1
        current_page_values = self.table_manager.get_current_page_values()
        self.show_items_from_db(current_page_values)

    def change_shown_category(self, *args):
        self.table_manager = TM(self.show_category())
        current_page_values = self.table_manager.get_current_page_values()
        self.show_items_from_db(current_page_values)


if __name__ == "__main__":
    gui = GUI()
    gui.draw_widgets()
    gui.root.mainloop()
