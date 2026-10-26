import pytest

from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected

def test_get_mask_account(account_number):
    assert get_mask_account(account_number) == expected
