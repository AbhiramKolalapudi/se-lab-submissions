
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


def test_dine_in_bill():
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_happy_hour():
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_large_group():
    assert bill_total("rooftop", 1000, 8, False) == 1417


def test_invalid_section():
    with pytest.raises(ValueError):
        bill_total("garden", 1000, 2, False)


def test_invalid_order():
    with pytest.raises(ValueError):
        bill_total("dine_in", -100, 2, False)


def test_even_split():
    assert split_bill(1000, 4, 10) == 275


def test_uneven_split():
    assert split_bill(100, 3, 0) == 34


def test_invalid_people():
    with pytest.raises(ValueError):
        split_bill(100, 0, 10)


def test_invalid_tip():
    with pytest.raises(ValueError):
        split_bill(100, 2, -5)


def test_call_ahead():
    assert table_wait(13, 2, False) == "call ahead"


def test_reserved_table():
    assert table_wait(4, 0, True) == "seat now"


def test_no_free_tables():
    assert table_wait(4, 0, False) == "waitlist"


def test_large_party_wait():
    assert table_wait(8, 1, False) == "waitlist"


def test_seat_now():
    assert table_wait(4, 2, False) == "seat now"
