# 1. Валидный payload как константа для прямых вызовов
VALID_BOOKING = {
    "firstname": "Automation",
    "lastname": "Tester",
    "totalprice": 1000,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-09-01",
        "checkout": "2025-09-10"
    },
    "additionalneeds": "Allure Report"
}

# 2. Данные для полного обновления (PUT)
UPDATE_BOOKING = {
    "firstname": "Super",
    "lastname": "Tester",
    "totalprice": 2000,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-10-01",
        "checkout": "2025-10-20"
    },
    "additionalneeds": "Espresso Machine"
}


# 3. Функция для параметризации негативных тестов
def invalid_booking_data():
    case1 = ({}, 500, "empty_payload")

    payload2 = VALID_BOOKING.copy()
    del payload2["firstname"]
    case2 = (payload2, 500, "missing_firstname")

    payload3 = VALID_BOOKING.copy()
    payload3["totalprice"] = "invalid_price"
    case3 = (payload3, 500, "invalid_totalprice_type")

    payload4 = VALID_BOOKING.copy()
    del payload4["bookingdates"]
    case4 = (payload4, 500, "missing_bookingdates")

    return [case1, case2, case3, case4]


def invalid_booking_data_ids():
    return [case[2] for case in invalid_booking_data()]

# 4. Данные для частичного обновления (PATCH)
PARTIAL_UPDATE_BOOKING = {
    "firstname": "James",
    "totalprice": 700
}

# Функция для параметризации негативных тестов с невалидными данными
def invalid_patch_data():
    """Возвращает данные для негативных PATCH тестов."""
    # Случай: Некорректный тип данных для 'depositpaid'
    case1 = ({"depositpaid": "not-a-boolean"}, 400, "invalid_depositpaid_type")
    return [case1]

def invalid_patch_data_ids():
    """Возвращает ID для параметризации."""
    return [case[2] for case in invalid_patch_data()]