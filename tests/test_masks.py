import pytest

from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture
def card_number():
    return["7000792289606361"]

@pytest.mark.parametrize(
    'card_number, expected',
    [("7000792289606361", "7000 79** **** 6361")],)

def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected

@pytest.mark.parametrize("card_number", ["1234", "", "   ",
        "1-2-3-4-5-6-7-8", "1234567890123", "123456789012345",
        "12345678901234567",],)
def test_get_mask_card_number_invalid_length(card_number):
    with pytest.raises(ValueError, match="ровно 16"):
        get_mask_card_number(card_number)


@pytest.fixture
def account_number():
    return ["73654108430135874305"]

@pytest.mark.parametrize(
    "account_number,expected",
    [("73654108430135874305", "** 4305")],)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected

@pytest.mark.parametrize("account_number", ["123", "", "   ", "1-2 3", "123"],)
def test_get_mask_account_invalid_number(account_number):
    with pytest.raises(ValueError):
        get_mask_account(account_number)
