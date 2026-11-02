# Проект "Генераторы"
### Описание:

Набор инструментов на Python для эффективной работы с
большими объёмами данных транзакций. Проект использует
генераторы для потоковой обработки данных — это
позволяет анализировать большие наборы транзакций без
загрузки всего массива в память.

### Основные возможности:

Фильтрация транзакций по коду валюты (filter_by_currency).
Генерация описаний транзакций (transaction_descriptions).
Генерация номеров карт в читаемом формате (card_number_generator).
Проект ориентирован на финансовых аналитиков и разработчиков,
которым нужно быстро извлекать и анализировать данные транзакций,
а также тестировать логику обработки.

### Установка:

1. ### Клонируйте репозиторий:
```
git clone https://github.com/username/generators.git
```

2. ### Создайте виртуальное окружение (рекомендуется):
```
python -m venv venv
#### Windows:
venv\Scripts\activate
#### macOS/Linux:
source venv/bin/activate
```

### 3. Установите зависимости:
```
pip install -r requirements.txt
```
Для тестов добавьте pytest и типы:
```
pip install pytest pytest-cov mypy
```
### 4. Проверьте установку и корректность типов
```
mypy src/
pytest
```
### Примечание:

В этом проекте нет базы данных и миграций — это
библиотека функций и генераторов, а не веб‑приложение.

### Использование:
```
from src.generators import filter_by_currency

transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
]

usd_transactions = list(filter_by_currency(transactions, "USD"))
usd_transactions содержит транзакции с id 1 и 3
```
### Пример генерации номеров карт
```
from src.generators import card_number_generator

for card in card_number_generator(1000, 1005):
    print(card)
# Вывод:
# 0000 0000 0000 1000
# 0000 0000 0000 1001
# ...
```
### Тестирование
Проект покрыт тестами с покрытием не менее 80 %.
### Для запуска:
```
pytest --cov=src --cov-report=term-missing
```

### Пример теста для 
 filter_by_currency:
```
import pytest
from src.generators import filter_by_currency

def test_filter_by_currency_returns_matching_transactions():
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3
```
