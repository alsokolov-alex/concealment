import pytest

from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture

def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected

@pytest.fixture

def test_get_mask_account(account_number):
    assert get_mask_account(account_number) == expected
