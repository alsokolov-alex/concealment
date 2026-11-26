import json
import pytest


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Пример корректного списка транзакций."""
    return [
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.475772",
            "operationAmount": {"amount": "67314.70", "currency": {"code": "RUB"}},
            "description": "Перевод организации",
            "from": "Счет 58833448650160897469",
            "to": "Счет 39283813393651161191",
        },
        {
            "id": 869168149,
            "state": "CANCELED",
            "date": "2019-11-15T06:24:02.659593",
            "operationAmount": {"amount": "43318.34", "currency": {"code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 58663923299526553195",
            "to": "Счет 45656261232452419245",
        },
    ]


@pytest.fixture
def sample_csv_content() -> str:
    """Содержимое CSV с разделителем ';' — как в файлах курса."""
    return (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703.0;EXECUTED;2023-09-05T11:30:32.370539;"
        "16210.0;Solana;SOL;Нет данных;Нет данных;Перевод с карты на карту\n"
        "359721.0;EXECUTED;2020-04-27T04:56:34.390466;"
        "433.0;Haltenbanken;NOK;Счет 57476641632865672732;"
        "Счет 74143617595277109398;Перевод организации\n"
    )
