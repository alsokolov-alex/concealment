import pytest

from src.widget import get_mask_account, get_date, get_mask_card_number, get_mask_account

@pytest.fixture

def test_mask_account_card(account_card, expected):
    assert mask_account_card(account_card) == expected

@pytest.fixture

def test_get_date(date_string, expected):
    assert get_date(date_string) == expected