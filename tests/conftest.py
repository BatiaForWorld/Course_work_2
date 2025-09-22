import json
import os
import tempfile
from unittest.mock import Mock

import pytest

from src.hh import HH
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def temp_json_file():
    """Создает временный JSON файл для тестов"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([], f)
        temp_file = f.name

    yield temp_file

    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def sample_vacancy_data():
    """Примеры данных вакансий для тестов"""
    return [
        {
            "id": "12345",
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/12345",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Python experience required"},
        },
        {
            "id": "67890",
            "name": "Java Developer",
            "alternate_url": "https://hh.ru/vacancy/67890",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "snippet": {"requirement": "Java experience required"},
        },
    ]


@pytest.fixture
def sample_vacancies():
    """Примеры объектов Vacancy для тестов"""
    return [
        Vacancy("1", "Python Developer", "url1", 100000, 150000, "RUR", "Python experience"),
        Vacancy("2", "Java Developer", "url2", 120000, 180000, "RUR", "Java experience"),
        Vacancy("3", "Python Senior", "url3", 200000, 250000, "RUR", "Senior Python developer"),
    ]


@pytest.fixture
def mock_json_saver(temp_json_file):
    """Мок JSONSaver с временным файлом"""
    return JSONSaver(temp_json_file)


@pytest.fixture
def mock_hh_api():
    """Мок HH API"""
    mock_saver = Mock()
    return HH(mock_saver)


@pytest.fixture
def mock_input():
    """Мок для input()"""
    import io
    import sys
    from contextlib import contextmanager

    @contextmanager
    def mock_user_input(inputs):
        """Контекст-менеджер для мока input() с последовательностью inputs"""
        input_iter = iter(inputs)

        def mock_input_func(prompt=""):
            try:
                value = next(input_iter)
                print(f"{prompt}{value}")
                return value
            except StopIteration:
                raise KeyboardInterrupt("No more input values provided")

        original_input = __builtins__["input"] if isinstance(__builtins__, dict) else __builtins__.input

        if isinstance(__builtins__, dict):
            __builtins__["input"] = mock_input_func
        else:
            __builtins__.input = mock_input_func

        try:
            yield
        finally:

            if isinstance(__builtins__, dict):
                __builtins__["input"] = original_input
            else:
                __builtins__.input = original_input

    return mock_user_input


@pytest.fixture
def mock_print():
    """Мок для print() с захватом вывода"""
    import io
    import sys
    from contextlib import contextmanager

    @contextmanager
    def capture_print():
        """Контекст-менеджер для захвата print()"""
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            yield captured_output
        finally:
            sys.stdout = old_stdout

    return capture_print


@pytest.fixture
def invalid_input_data():
    """Данные для тестирования некорректного ввода"""
    return {
        "empty_strings": ["", "   ", "\t", "\n"],
        "invalid_numbers": ["abc", "-1", "0", "1.5", "10abc", "abc10"],
        "invalid_choices": ["-1", "7", "10", "abc", ""],
        "invalid_salaries": ["abc", "100000-", "-150000", "150000-100000", "abc-def"],
        "special_chars": ["!@#$", "возраст 25", "зарплата от 100к"],
    }


@pytest.fixture
def complex_vacancy_scenarios():
    """Сложные сценарии с вакансиями для тестирования"""
    return {
        "empty_list": [],
        "single_vacancy": [Vacancy("1", "Python Developer", "url1", 100000, 150000, "RUR", "Python experience")],
        "vacancies_without_salary": [
            Vacancy("1", "Junior Developer", "url1", 0, 0, "", "Entry level"),
            Vacancy("2", "Intern", "url2", 0, 0, "", "No experience needed"),
        ],
        "mixed_salary_vacancies": [
            Vacancy("1", "Python Developer", "url1", 100000, 150000, "RUR", "Python experience"),
            Vacancy("2", "Java Developer", "url2", 0, 0, "", "Java experience"),
            Vacancy("3", "Senior Python", "url3", 200000, 250000, "RUR", "Senior level"),
        ],
        "large_dataset": [
            Vacancy(
                str(i),
                f"Developer {i}",
                f"url{i}",
                50000 + i * 1000,
                100000 + i * 1000,
                "RUR",
                f"Experience {i} years",
            )
            for i in range(1, 101)
        ],
        "duplicate_ids": [
            Vacancy("1", "Python Developer", "url1", 100000, 150000, "RUR", "Python"),
            Vacancy("1", "Java Developer", "url2", 120000, 180000, "RUR", "Java"),
        ],
    }


@pytest.fixture
def api_error_scenarios():
    """Сценарии ошибок API для тестирования"""
    return {
        "network_error": Exception("Network connection failed"),
        "api_error": Exception("API request failed with status 500"),
        "timeout_error": Exception("Request timeout"),
        "json_decode_error": Exception("Failed to decode JSON response"),
        "empty_response": [],
        "malformed_data": [{"invalid": "data"}],
    }


@pytest.fixture
def file_error_scenarios():
    """Сценарии файловых ошибок для тестирования"""
    return {
        "file_not_found": FileNotFoundError("File not found"),
        "permission_denied": PermissionError("Permission denied"),
        "json_decode_error": json.JSONDecodeError("Invalid JSON", "", 0),
        "disk_full": OSError("No space left on device"),
    }
