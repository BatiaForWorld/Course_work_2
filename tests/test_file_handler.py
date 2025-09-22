from abc import ABC

import pytest

from src.file_handler import FileHandler


class TestFileHandler:
    """Тесты для абстрактного класса FileHandler"""

    def test_file_handler_is_abstract(self):
        """Тест что FileHandler является абстрактным классом"""
        assert issubclass(FileHandler, ABC)

    def test_file_handler_cannot_be_instantiated(self):
        """Тест что FileHandler нельзя инстанцировать напрямую"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            FileHandler()

    def test_file_handler_abstract_methods(self):
        """Тест наличия всех абстрактных методов"""
        abstract_methods = {
            "add_vacancy",
            "delete_vacancy",
            "filter_vacancies",
            "filter_vacancies_by_salary",
            "get_all_vacancies",
        }

        actual_abstract_methods = set(FileHandler.__abstractmethods__)

        assert actual_abstract_methods == abstract_methods

    def test_concrete_file_handler_implementation(self):
        """Тест что конкретная реализация FileHandler работает"""

        class ConcreteFileHandler(FileHandler):
            def __init__(self):
                self.data = []

            def add_vacancy(self, vacancy_data):
                self.data.append(vacancy_data)

            def delete_vacancy(self, vacancy_id):
                self.data = [v for v in self.data if v.get("id") != vacancy_id]

            def filter_vacancies(self, filter_words):
                return [
                    v for v in self.data if any(word.lower() in v.get("name", "").lower() for word in filter_words)
                ]

            def filter_vacancies_by_salary(self, salary_range):
                min_salary, max_salary = salary_range
                result = []
                for v in self.data:
                    salary_from = v.get("salary_from", 0) or 0
                    salary_to = v.get("salary_to", 0) or 0
                    avg = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
                    if min_salary <= avg <= max_salary:
                        result.append(v)
                return result

            def get_all_vacancies(self):
                return self.data

        handler = ConcreteFileHandler()
        vacancy = {"id": "1", "name": "Python Developer", "salary_from": 100000, "salary_to": 150000}
        handler.add_vacancy(vacancy)
        assert len(handler.get_all_vacancies()) == 1

        filtered_result = handler.filter_vacancies(["Python"])
        assert len(filtered_result) == 1

        salary_filtered = handler.filter_vacancies_by_salary((100000, 200000))
        assert len(salary_filtered) == 1

        handler.delete_vacancy("1")
        assert len(handler.get_all_vacancies()) == 0
