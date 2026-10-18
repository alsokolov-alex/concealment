from processing import filter_by_state
# Выход функции со статусом по умолчанию 'EXECUTED'
data = [
{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

# Фильтрация по умолчанию (state='EXECUTED')
executed_only = filter_by_state(data)
print("Только EXECUTED:")
for item in executed_only:
    print(item)

# Фильтрация по CANCELED
canceled_only = filter_by_state(data, 'CANCELED')
print("\nТолько CANCELED:")
for item in canceled_only:
    print(item)
  
