# ui/test_data/form_data.py

def invalid_form_data():
    """
    Данные для негативных тестов формы.
    Формат: (first_name, last_name, email, field_to_check_name, test_id)
    """
    # Кейс 1: Пустое поле First Name
    case1 = ("", "ValidLastName", "valid@email.com", "first_name", "empty_first_name")

    # Кейс 2: Пустое поле Last Name
    case2 = ("ValidFirstName", "", "valid@email.com", "last_name", "empty_last_name")

    # Кейс 3: Невалидный Email (без @)
    case3 = ("ValidFirstName", "ValidLastName", "invalid-email.com", "email", "invalid_email_format")

    # Кейс 4: Невалидный Email (без домена)
    case4 = ("ValidFirstName", "ValidLastName", "invalid@", "email", "invalid_email_no_domain")

    return [case1, case2, case3, case4]


# V-- ИЗМЕНЯЕМ ЭТУ ФУНКЦИЮ --V
def get_invalid_data_ids():
    """
    Возвращает ГОТОВЫЙ СПИСОК ID для параметризации.
    """
    # Мы просто извлекаем пятый элемент (test_id) из каждого набора данных
    return [item[4] for item in invalid_form_data()]
