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
        self.user_input = tk.StringVar(self.root)

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

        self.starting_pos = 1
        self.in_bookmarked = False

    def show_category(self):
        category = self.clicked.get()
        self.category_label.config(text=self.clicked.get())
        return category

    def draw_widgets(self):
        pages = ""

        # Input field
        username_label = ttk.Entry(self.root, textvariable=self.user_input, font=("", 24))
        username_label.grid(column=0, row=0, columnspan=4, sticky=tk.EW, padx=60, pady=5)

        # Dropdown menu for to choose the category
        self.clicked.set("Category")
        drop_menu = tk.OptionMenu(self.root, self.clicked, *self.options)
        drop_menu.configure(width=15, height=3)
        drop_menu.grid(column=4, row=0, sticky=tk.EW, padx=5, pady=5)
        self.category_label = ttk.Label(self.root, text=" ")

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
        bookmark_btn = tk.Button(self.root, text="aaa",
                                 command=self.show_bookmarked_items,
                                 image=tk_image, width=50, height=50)
        bookmark_btn.image = tk_image
        bookmark_btn.grid(column=7, row=0, sticky=tk.W, padx=5, pady=5)

        # The Label for the current page counter
        self.pages = tk.Label(self.root, text=pages,
                              background='pink')
        self.pages.grid(column=3, row=2, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # The buttons to cycle the the category left and right
        next_page_btn = tk.Button(self.root, text="Next page",
                                  command=self.get_next_items,
                                  width=15, height=3)
        next_page_btn.grid(column=5, row=2, sticky=tk.W, padx=5, pady=5)
        previouse_page_btn = tk.Button(self.root, text="Previouse page",
                                       command=self.get_previous_items,
                                       width=15, height=3)
        previouse_page_btn.grid(column=2, row=2, sticky=tk.E, padx=5, pady=5)

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

        current_names = []
        current_names.clear()

        # get item with the according to the current i value + the page counter min
        for i, item in enumerate(current_values):

            i = i + 1

            if item != []:
                current_names.append(item.item_name)

            search_btn = tk.Label(self.root, text="Image", background='gray79', image=tk_image)
            search_btn.grid(column=2, row=1 + 2 * i + (i - 1), rowspan=3, sticky=tk.NSEW,
                            padx=5, pady=5)

            item_name = tk.Label(self.root, text=name, font=("", 14), background='red')
            item_name.grid(column=3, row=1 + 2 * i + (i - 1), columnspan=3, sticky=tk.NSEW,
                           padx=2, pady=5)

            item_price = tk.Label(self.root, text=price,
                                  font=("", 10), background='green')
            item_price.grid(column=3, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)

            item_pps = tk.Label(self.root, text=pps,
                                font=("", 10), background='light blue')
            item_pps.grid(column=4, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)

            item_hdc = tk.Label(self.root, text=change,
                                font=("", 10), background='yellow')
            item_hdc.grid(column=5, row=2 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)

            item_tp = tk.Label(self.root, text=trader_name,
                               font=("", 10), background='yellow')
            item_tp.grid(column=3, row=3 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)

            item_tn = tk.Label(self.root, text=trader_price,
                               font=("", 10), background='yellow')
            item_tn.grid(column=4, row=3 + 2 * i + (i - 1), sticky=tk.NSEW, padx=2, pady=2)

            if item != []:
                item_name.config(text=item.item_name)
                item_price.config(text=item.price)
                item_pps.config(text=item.price_per_slot)
                item_hdc.config(text=str(item.h_change + " / " + item.d_change))
                item_tp.config(text=item.trader_price)
                item_tn.config(text=item.trader_name)
            else:
                item_name.config(text="")
                item_price.config(text="")
                item_pps.config(text="")
                item_hdc.config(text="")
                item_tp.config(text="")
                item_tn.config(text="")

        if self.in_bookmarked:
            self.show_remove_buttons(current_names)
        else:
            self.show_bookmark_buttons(current_names, True)

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
                current_page_values = self.table_manager \
                    .get_current_page_values(1,
                                             self.user_input.get())
                if current_page_values != []:
                    self.show_items_from_db(current_page_values)
                    self.pages.config(text=str(self.starting_pos) + " >-< " +
                                      str(self.starting_pos + 6))
                break

    def update_btn_function(self):
        self.in_bookmarked = False
        checking_task = threading.Thread(target=self.check_if_still_downloading)
        print(self.show_category())
        checking_task.start()

    def get_next_items(self):
        self.in_bookmarked = False
        # basically do this
        # self.current_page_values = table_manager.get_current_page_values()

        # or just do start_pos += 7
        self.starting_pos += 7
        current_page_values = self.table_manager.get_current_page_values(self.starting_pos,
                                                                         self.user_input.get())
        if current_page_values != []:
            self.show_items_from_db(current_page_values)
            self.pages.config(text=str(self.starting_pos) + " >-< " +
                              str(self.starting_pos + 6))

    def get_previous_items(self):
        self.in_bookmarked = False
        # basically do this
        # self.current_page_values = table_manager.get_current_page_values()

        # or just do start_pos -= 7
        self.starting_pos -= 7
        if self.starting_pos < 1:
            self.starting_pos = 1
        current_page_values = self.table_manager.get_current_page_values(self.starting_pos,
                                                                         self.user_input.get())
        if current_page_values != []:
            self.show_items_from_db(current_page_values)
            self.pages.config(text=str(self.starting_pos) + " >-< " +
                              str(self.starting_pos + 6))

    def change_shown_category(self, *args):
        self.in_bookmarked = False
        self.starting_pos = 1
        self.table_manager = TM(self.show_category())
        current_page_values = self.table_manager.get_current_page_values(1,
                                                                         self.user_input.get())
        if current_page_values != []:
            self.show_items_from_db(current_page_values)
            self.pages.config(text=str(self.starting_pos) + " >-< " +
                              str(self.starting_pos + 6))

    def add_item_to_bookmark(self, item_name):
        self.table_manager.add_item_to_bookmark(item_name)

    def show_remove_buttons(self, current_names):

        btn_width = 10

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[0]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=3, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[1]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=6, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[2]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=9, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[3]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=12, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[4]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=15, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[5]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=18, sticky=tk.W)

        remove_btn = tk.Button(self.root, text="remove",
                               command=lambda: self.remove_item_from_bookmark(current_names[6]),
                               font=("", 8), background='red2', width=btn_width)
        remove_btn.grid(column=6, row=21, sticky=tk.W)

    def show_bookmark_buttons(self, current_names, visit_for_delete):

        btn_width = 10

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[0]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=3, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[1]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=6, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[2]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=9, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[3]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=12, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[4]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=15, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[5]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=18, sticky=tk.W)

        bookmark_btn = tk.Button(self.root, text="bookmark",
                                 command=lambda: self.add_item_to_bookmark(current_names[6]),
                                 font=("", 8), background='light blue', width=btn_width)
        bookmark_btn.grid(column=6, row=21, sticky=tk.W)

    def show_bookmarked_items(self):
        self.in_bookmarked = True
        current_page_values = self.table_manager.get_bookmarked_entries(1,
                                                                        self.user_input.get())
        if current_page_values != []:
            self.show_items_from_db(current_page_values)
            self.pages.config(text=str(self.starting_pos) + " >-< " +
                              str(self.starting_pos + 6))

    def remove_item_from_bookmark(self, item_name):
        self.in_bookmarked = True
        self.table_manager.remove_item_from_bookmark(item_name)
        self.show_bookmarked_items()
