"""Insert the values that were downloaded."""

import sqlalchemy as sql
from src.downloader import Downloader
from src.models import ActiveEntries, Base, Categories, Entries, Bookmarked
from sqlalchemy.orm import sessionmaker


class TableManagement():
    def __init__(self, category) -> None:

        self.category = category.lower().replace(" ", "_")

        engine = sql.create_engine("sqlite:///database/database.db", echo=False)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def search_for_items(self):
        """Returns the data from the website and save it into a file."""
        url_extension = "tag/" + self.category.lower().replace(" ", "_")
        downloader = Downloader(url_extension)
        downloader.get_page_content()
        extracted_valued = downloader.extract_values("webpage.html")

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

    def get_current_page_values(self, starting_pos, item_name_snippet):
        item_name_snippet = str("%" + item_name_snippet + "%")

        category_id = self.get_category_id()

        active_category = self.session.query(ActiveEntries) \
            .filter_by(category_id=category_id).first()

        # At first active_category is always None so I have to do it separately
        if active_category is not None:
            active_category = active_category.category_id
        # with this the lag while scrolling "next" and "previous" is gone
        # if category_id != active_category:
        self.create_active_entries()
        database = self.session.query(Entries).filter_by(category_id=category_id).first()
        if database is None:
            return []

        current_values = self.insert_into_active_entries(starting_pos, item_name_snippet)
        return current_values

    def add_item_to_bookmark(self, item_name):
        print(item_name)
        item = self.session.query(Entries).filter_by(item_name=item_name).first()
        item_count = self.session.query(Bookmarked).filter_by(entry_id=item.id).count()

        if item_count > 0:
            return
        bookmark = Bookmarked(entry_id=item.id)
        self.session.add(bookmark)
        self.session.commit()

    def remove_item_from_bookmark(self, item_name):
        print("removed: " + item_name)
        item = self.session.query(Entries).filter_by(item_name=item_name).first()
        self.session.query(Bookmarked).filter_by(entry_id=item.id).delete()
        self.session.commit()

    def get_bookmarked_entries(self, starting_pos, item_name_snippet):
        item_name_snippet = str("%" + item_name_snippet + "%")

        all_ids = self.session.query(Bookmarked).all()
        self.session.query(ActiveEntries).delete()

        # this_category_id = self.get_category_id()
        max_entries = self.session.query(Bookmarked).count()
        if starting_pos > max_entries:
            starting_pos = max_entries - 7

        for item in all_ids:
            entry = self.session.query(Entries).filter_by(id=item.entry_id).first()
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

        current_values = self.insert_into_active_entries(starting_pos, item_name_snippet)
        return current_values

    def insert_into_active_entries(self, starting_pos, item_name_snippet):
        starting_pos -= 1
        current_values = []
        counter = 0

        # this_category_id = self.get_category_id()
        max_entries = self.session.query(ActiveEntries) \
            .filter(ActiveEntries.item_name.like(item_name_snippet)).count()

        if starting_pos > max_entries:
            starting_pos = max_entries - 7

        while current_values.__len__() < 7 and starting_pos + counter <= max_entries:
            entry = self.session.query(ActiveEntries) \
                .filter(ActiveEntries.id == starting_pos + counter,
                        ActiveEntries.item_name.like(item_name_snippet)).first()
            if entry is not None:
                current_values.append(entry)
            counter += 1

        while current_values.__len__() < 7:
            current_values.append([])

        return current_values
