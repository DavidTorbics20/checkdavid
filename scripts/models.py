"""The schemes for all tables"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Categories(Base):
    __tablename__ = "Categories"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)

    def __init__(self, name):
        self.name = name


class Entries(Base):
    __tablename__ = "Entries"

    id = Column("id", Integer, primary_key=True)
    category_id = Column("category_id", Integer, ForeignKey(Categories.id))
    item_name = Column("item name", String)
    # for the time being just use some random image here
    # - not that from tarkov-market
    # item_image =
    price = Column("price", String)
    price_per_slot = Column("price per slot", String)
    h_change = Column("hour change", String)
    d_change = Column("day change", String)
    trader_name = Column("trader name", String)
    trader_price = Column("trader price", String)
    # bring bach the bookmarked column


class ActiveEntries(Base):
    __tablename__ = "ActiveEntries"

    id = Column("id", Integer, primary_key=True)
    item_name = Column("item name", String)
    # for the time being just use some random image here
    # - not that from tarkov-market
    # item_image =
    price = Column("price", String)
    price_per_slot = Column("price per slot", String)
    h_change = Column("hour change", String)
    d_change = Column("day change", String)
    trader_price = Column("trader price", String)
    trader_name = Column("trader name", String)
    # bring bach the bookmarked column


class Bookmarked(Base):
    __tablename__ = "Bookmarked"

    id = Column("id", Integer, primary_key=True)
    entry_id = Column("entry_id", Integer, ForeignKey(Entries.id))
