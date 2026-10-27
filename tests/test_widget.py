import pytest

from src.widget import get_mask_account, get_date, get_mask_card_number, mask_account_card


@pytest.fixture

def test_mask_account_card(account_card: str, expected: str) -> None:
    assert mask_account_card(account_card) == expected


@pytest.fixture

def test_get_date(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected
