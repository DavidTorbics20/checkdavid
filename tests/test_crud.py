"""Test the functionality of table_management.py."""


from src.table_management import TableManagement
from src.models import Bookmarked, Categories, Entries
from random_word import RandomWords


def test_table_management_01_downloader_exists():
    """Test if the Downloader class is implemented."""
    assert TableManagement


def test_table_management_02_add_to_bookmark():
    table_management = TableManagement("ammo")
    assert table_management

    table_management.session.query(Bookmarked).delete()
    first_item_count = table_management.session.query(Bookmarked).count()
    table_management.add_item_to_bookmark("9x39mm SP-6 gs")
    second_item_count = table_management.session.query(Bookmarked).count()
    assert (first_item_count + 1) == second_item_count


def test_table_management_03_delete_from_bookmark():
    table_management = TableManagement("ammo")
    assert table_management

    table_management.add_item_to_bookmark("9x39mm SP-6 gs")
    first_item_count = table_management.session.query(Bookmarked).count()
    table_management.remove_item_from_bookmark("9x39mm SP-6 gs")
    second_item_count = table_management.session.query(Bookmarked).count()
    assert (first_item_count - 1) == second_item_count


def test_table_management_04_get_bookmarked_entries():
    table_management = TableManagement("ammo")
    assert table_management

    table_management.session.query(Bookmarked).delete()
    table_management.add_item_to_bookmark("9x39mm SP-6 gs")
    table_management.add_item_to_bookmark("9x21mm BT gzh")
    table_management.add_item_to_bookmark("PU 3.5x riflescope")
    result = table_management.get_bookmarked_entries(1, "")
    assert result.__len__() == 7

    for i in range(7):
        if i < 3:
            assert result[i] != []
        else:
            assert result[i] == []

    assert result[0].item_name == "9x39mm SP-6 gs"
    assert result[1].item_name == "9x21mm BT gzh"
    assert result[2].item_name == "PU 3.5x riflescope"


def test_table_management_05_item_in_bookmarked_only_once():
    table_management = TableManagement("containers")
    assert table_management

    first_item_count = table_management.session.query(Bookmarked).count()
    table_management.add_item_to_bookmark("Money case")
    second_item_count = table_management.session.query(Bookmarked).count()
    assert (first_item_count + 1) == second_item_count

    table_management.add_item_to_bookmark("Money case")
    assert (first_item_count + 1) == second_item_count


def test_table_management_06_creating_categories():
    table_management = TableManagement("ammo")
    assert table_management

    table_management.session.query(Categories).delete()
    table_management.create_categories()
    category_count = table_management.session.query(Categories).count()
    assert category_count == 18


def test_table_management_07_add_item_to_entries():
    table_management = TableManagement("ammo")
    assert table_management

    random_name = RandomWords()

    # Return a single random word
    random_item_name = random_name.get_random_word()

    first_item_count = table_management.session.query(Entries).count()
    test_values = [random_item_name, "free", "free", "0%", "0%", "Jeff", "free"]
    table_management.add_item_to_entries(test_values, 3)
    second_item_count = table_management.session.query(Entries).count()
    table_management.session.commit()
    assert (first_item_count + 1) == second_item_count

    table_management.session.query(Entries).filter_by(item_name=random_item_name).delete()
    third_item_count = table_management.session.query(Entries).count()
    table_management.session.commit()
    assert first_item_count == third_item_count


def test_table_management_08_get_category_id():
    table_management = TableManagement("ammo")
    assert table_management

    category_id = table_management.get_category_id()
    assert category_id == 10
