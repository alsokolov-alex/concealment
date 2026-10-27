import pytest

from src.widget import get_mask_account, get_date, get_mask_card_number, mask_account_card


@pytest.fixture
def test_account_masking():
    result = mask_account_card("счёт 73654108430135874305")
    assert result.startswith("счёт ")
    assert result.endswith("** 4305")

def test_account_with_uppercase():
    result = mask_account_card("СЧЁТ 73654108430135874305")
    assert "счёт" in result.lower() and result.endswith("** 4305")

def test_card_masking_valid():
    result = mask_account_card("карта 4111111111111111")
    assert result.startswith("карта ")
    assert result.endswith("**** 1111")

def test_invalid_type():
    result = mask_account_card(12345)
    assert "Некорректный ввод" in result

def test_empty_string():
    assert "Укажите тип и номер" in mask_account_card("")

def test_only_spaces():
    assert "Укажите тип и номер" in mask_account_card("   ")

def test_missing_number():
    assert "Укажите тип и номер" in mask_account_card("счёт")
    assert "Укажите тип и номер" in mask_account_card("карта")

def test_non_digit_number():
    assert "Некорректный номер" in mask_account_card("карта abc123")
    assert "Некорректный номер" in mask_account_card("счёт 12a34")

def test_short_account_number():
    result = mask_account_card("счёт 123")
    assert "Некорректный номер счёта" in result

def test_wrong_card_length():
    result = mask_account_card("карта 123456789012345")  # 15 цифр
    assert "Некорректный номер карты" in result

def test_multiple_spaces():
    result = mask_account_card("счёт   73654108430135874305")
    assert result.endswith("** 4305")

def test_prefix_with_multiple_words():
    result = mask_account_card("тип счёта 73654108430135874305")
    assert "тип счёта" in result
    assert result.endswith("** 4305")

@pytest.fixture
def test_valid_iso_datetime():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2000-01-01T00:00:00.000000") == "01.01.2000"
    assert get_date("2099-12-31T23:59:59.999999") == "31.12.2099"

def test_single_digit_month_and_day_still_correct():
    # strptime корректно обработает ведущие нули в формате
    assert get_date("2024-03-05T10:10:10.123456") == "05.03.2024"

def test_invalid_type():
    with pytest.raises(ValueError):
        get_date(123)
    with pytest.raises(ValueError):
        get_date(None)  # если передадут None, тоже будет ошибка

def test_empty_string():
    with pytest.raises(ValueError):
        get_date("")

def test_wrong_format():
    # Не хватает миллисекунд
    with pytest.raises(ValueError):
        get_date("2024-03-11T02:26:18")
    # Другой разделитель
    with pytest.raises(ValueError):
        get_date("2024/03/11T02:26:18.671407")
    # Перепутаны части
    with pytest.raises(ValueError):
        get_date("11-03-2024T02:26:18.671407")

def test_too_short_string():
    with pytest.raises(ValueError):
        get_date("2024")