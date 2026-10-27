import pytest

from src.masks import get_mask_card_number, get_mask_account
from typing import Any, Dict, List


@pytest.fixture
def card_number():
    return ["7000792289606361"]


@pytest.fixture
def account_number():
    return ["73654108430135874305"]


@pytest.fixture
def state():
    return ["EXECUTED", "CANCELED"]


@pytest.fixture
def date():
    return ["2019-07-03T18:35:29.512364", "2024-03-11T02:26:18.671407", "11.03.2024", "02.07.2019"]


@pytest.fixture
def account_card():
    return [
        "Visa Platinum 7000792289606361" "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]


@pytest.fixture
def lists():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]


@pytest.fixture
def records():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
            ]


@pytest.fixture
def expected():
    return [
        "Visa Platinum 7000 79** **** 6361",
        "Maestro 1596 83** **** 5199",
        "MasterCard 7158 30** **** 6758",
        "Visa Classic 6831 98** **** 7658",
        "Visa Platinum 8990 92** **** 5229",
        "Visa Gold 5999 41** **** 6353",
        "Счет **5560",
        "Счет **9589",
        "Счет **4305",
        "EXECUTED",
        "CANCELED",
        "11.03.2024",
        "02.07.2019",
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
           ]

@pytest.fixture
def INVALID_CARD_NUMBERS():
    return [
    "1234",
    "",
    "   ",
    "1-2-3-4-5-6-7-8",
    "1234567890123",
    "123456789012345",
    "12345678901234567",
]