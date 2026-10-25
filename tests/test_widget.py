import pytest

from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture
def account_card():
    return[Maestro 1596837868705199]
def date_string():
    return[2024-03-11T02:26:18.671407]

@pytest.mark.parametrize('account_card, expected', [(Maestro 1596837868705199), (Maestro 1596 83** **** 5199)])

def test_mask_account_card(account_card, expected):
    assert mask_account_card(account_card) == expected

@pytest.mark.parametrize('date_string, expected', [(2024-03-11T02:26:18.671407), (11.03.2024)])

    def test_get_date(date_string, expected):
    assert get_date(date_string) == expected