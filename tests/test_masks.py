import pytest

from src.masks import get_mask_card_number, get_mask_account


@pytest.fixture

@pytest.mark.parametrize('expected', ["7000 79** **** 6361"])

def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.fixture

@pytest.mark.parametrize(' expected', ["**4305"])

def test_get_mask_account(account_number: str, expected: str) -> None:
    assert get_mask_account(account_number) == expected
