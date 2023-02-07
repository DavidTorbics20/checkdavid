"""Insert the values that were downloaded."""

import threading

import sqlalchemy as sql
from downloader import Downloader
from models import ActiveEntries, Base, Categories, Entries
from sqlalchemy.orm import sessionmaker


class TableManagement():
    def __init__(self, category) -> None:

        self.category = category.lower().replace(" ", "_")

        engine = sql.create_engine("sqlite:///database/database.db", echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

        # This in a sepparate thread.
        # downloader = Downloader
        # for category in options:
        #     downloader = Downloader(category.lower().replace(" ", "_"))
        #     downloader.get_page_content()
        #     extracted_valued = downloader.extract_values()
        #     downloader.get_values_from_extraction(extracted_valued)

    def search_for_items(self):
        """Returns the data from the website and save it into a file."""
        url_extension = "tag/" + self.category.lower().replace(" ", "_")
        downloader = Downloader(url_extension)
        downloader.get_page_content()
        extracted_valued = downloader.extract_values()

        category_id = self.get_category_id()

        for intX, item in enumerate(extracted_valued):
            refined_values = downloader.get_values_from_extraction(intX, item)
            self.add_or_update(refined_values, category_id)

        self.session.close()
        # return the currently active category list

    def add_or_update(self, refined_values, category_id):

        database = self.session.query(Entries).filter_by(item_name=refined_values[0]).first()

        if database is None:
            self.add_item_to_entries(refined_values, category_id)
        else:
            self.update_values_in_entries(refined_values)

    def add_item_to_entries(self, refined_values, category_id):

        entry = Entries(category_id=category_id,
                        item_name=refined_values[0],
                        price=refined_values[1],
                        price_per_slot=refined_values[2],
                        h_change=refined_values[3],
                        d_change=refined_values[4],
                        trader_price=refined_values[5],
                        trader_name=refined_values[6])

        self.session.add(entry)
        self.session.commit()

    def update_values_in_entries(self, refined_values):
        entry = self.session.query(Entries).filter_by(item_name=refined_values[0]).first()

        entry.item_name = refined_values[0]
        entry.price = refined_values[1]
        entry.price_per_slot = refined_values[2]
        entry.h_change = refined_values[3]
        entry.d_change = refined_values[4]
        entry.trader_price = refined_values[5]
        entry.trader_name = refined_values[6]

        self.session.commit()

    def get_category_id(self):
        database = self.session.query(Categories).filter_by(name=self.category).first()

        if database is None:
            self.create_categories()

        category_id = self.session.query(Categories).filter_by(name=self.category).first().id

        return category_id

    def create_categories(self):
        """Create the categories in case they don't exist yet."""
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

        for option in options:
            options_str = option.lower().replace(" ", "_")
            category = Categories(name=options_str)
            self.session.add(category)
            self.session.commit()

    def create_active_entries(self):
        """Clone the Entries table but just with the current category
        select * from entries e join on activeentries ae where ae.id = e.id
        sowas"""
        current_category = self.get_category_id()
        entries = self.session.query(Entries).filter_by(category_id=current_category)
        self.session.query(ActiveEntries).delete()
        for entry in entries:
            active_entry = ActiveEntries(category_id=entry.category_id,
                                         item_name=entry.item_name,
                                         price=entry.price,
                                         price_per_slot=entry.price_per_slot,
                                         h_change=entry.h_change,
                                         d_change=entry.d_change,
                                         trader_price=entry.trader_price,
                                         trader_name=entry.trader_name)
            self.session.add(active_entry)
            self.session.commit()

    def get_current_page_values(self, starting_pos):
        current_values = []
        category_id = self.get_category_id()

        active_category = self.session.query(ActiveEntries) \
            .filter_by(category_id=category_id).first()

        # this is unnecessary
        if active_category is not None:
            active_category = active_category.category_id

        if category_id != active_category:
            self.create_active_entries()

        database = self.session.query(Entries).filter_by(category_id=category_id).first()
        if database is None:
            return current_values

        # this_category_id = self.get_category_id()
        max_entries = self.session.query(ActiveEntries).count()
        if starting_pos > max_entries:
            starting_pos = max_entries

        for i in range(0, 7):
            entry = self.session.query(ActiveEntries).filter_by(id=starting_pos + i).first()
            if entry is not None:
                print(entry.item_name)
                current_values.append(entry)

        return current_values
