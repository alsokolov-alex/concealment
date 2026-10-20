from src.processing import filter_by_state, sort_by_date
# Выход функции со статусом по умолчанию 'EXECUTED'

data = [
{'id': 414288290, 'state': 'CANCELED', 'date': '2019-07-03T18:35:29.512364'},
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
]

# Тип переменной выводится как List[Dict[str, Any]]
executed_only = filter_by_state(data, 'EXECUTED')

# Сортировка по убыванию (по умолчанию)
sorted_by_date_desc = sort_by_date(data)

# Сортировка по возрастанию
sorted_by_date_asc = sort_by_date(data, descending=False)

# Комбинация: сначала фильтр, потом сортировка
filtered_and_sorted = sort_by_date(filter_by_state(data, 'EXECUTED'))

executed_only = filter_by_state(data)
print("Только EXECUTED:")
for item in executed_only:
    print(item)

print(filtered_and_sorted)
