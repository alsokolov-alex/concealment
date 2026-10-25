import pytest

from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture
def card_number():
    return[7000792289606361]

def account_number():
    return[73654108430135874305]

def account_card():
    return[(Maestro 1596837868705199),
           (Счет 64686473678894779589),
           (MasterCard 7158300734726758),
           (Счет 35383033474447895560),
           (Visa Classic 6831982476737658),
           (Visa Platinum 8990922113665229),
           (Visa Gold 5999414228426353),
           (Счет 73654108430135874305)
           ]