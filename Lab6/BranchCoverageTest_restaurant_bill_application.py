
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# BILL TOTAL TESTS

def test_dine_in_bill():
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_happy_hour():
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_large_group():
    assert bill_total("dine_in", 1000, 8, False) == 1365


def test_invalid_section():
    with pytest.raises(ValueError):
        bill_total("garden", 1000, 2, False)


def test_invalid_order():
    with pytest.raises(ValueError):
        bill_total("dine_in", -100, 2, False)


def test_invalid_guest_count():
    with pytest.raises(ValueError):
        bill_total("dine_in", 1000, 0, False)


def test_takeaway_happy_hour():
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_takeaway_normal():
    assert bill_total("takeaway", 1000, 2, False) == 1050


def test_zero_food_total():
    assert bill_total("dine_in", 0, 2, False) == 0


def test_group_below_threshold():
    assert bill_total("dine_in", 1000, 7, False) == 1155


def test_group_at_threshold():
    assert bill_total("dine_in", 1000, 8, False) == 1365


# SPLIT BILL TESTS

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


# TABLE WAIT TESTS

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


def test_large_party_with_enough_tables():
    assert table_wait(8, 2, False) == "seat now"


def test_small_party_one_table():
    assert table_wait(4, 1, False) == "seat now"


def test_party_size_boundary():
    assert table_wait(12, 2, False) == "seat now"


def test_reservation_large_party():
    assert table_wait(13, 2, True) == "call ahead"
