def filter_by_state(lists, state="EXECUTED"):
    """
    Возвращает новый список словарей, где значение ключа 'state' равно указанному.

    :param lists: список словарей (например, список транзакций/задач)
    :param state: строка со значением state (по умолчанию 'EXECUTED')
    :return: отфильтрованный список словарей
    """

    result = []
    for data_list in lists:
        # Проверяем, есть ли ключ 'state' и совпадает ли его значение с нужным
        if data_list.get("state") == state:
            result.append(data_list)
    return result


from datetime import datetime


def sort_by_date(records, descending=True):
    """
    Сортирует список словарей по полю 'date'.

    Параметры:
        records: список словарей, у каждого есть ключ 'date' со строкой в формате ISO
        descending: если True — сортировка по убыванию (сначала самые новые), иначе по возрастанию

    Возвращает:
        Новый отсортированный список (исходный не меняется).
    """

    def parse_date(item):
        # Превращаем строку даты в объект datetime для корректной сортировки
        return datetime.fromisoformat(item["date"])

    # sorted возвращает новый список, не меняя исходный
    return sorted(records, key=parse_date, reverse=descending)
