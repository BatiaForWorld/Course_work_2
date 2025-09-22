import pytest

from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_init_valid(self):
        """Тест инициализации вакансии с валидными данными"""
        vacancy = Vacancy(
            id="12345",
            name="Python Developer",
            alternate_url="https://hh.ru/vacancy/12345",
            salary_from=100000,
            salary_to=150000,
            salary_currency="RUR",
            requirement="Python experience required",
        )

        assert vacancy.id == "12345"
        assert vacancy.name == "Python Developer"
        assert vacancy.alternate_url == "https://hh.ru/vacancy/12345"
        assert vacancy.salary_from == 100000.0
        assert vacancy.salary_to == 150000.0
        assert vacancy.salary_currency == "RUR"
        assert vacancy.requirement == "Python experience required"

    def test_vacancy_init_invalid_id(self):
        """Тест инициализации с невалидным ID"""
        with pytest.raises(ValueError):
            Vacancy(
                id="",
                name="Python Developer",
                alternate_url="https://hh.ru/vacancy/12345",
                salary_from=100000,
                salary_to=150000,
                salary_currency="RUR",
                requirement="Python experience required",
            )

    def test_vacancy_init_invalid_name(self):
        """Тест инициализации с невалидным именем"""
        with pytest.raises(ValueError):
            Vacancy(
                id="12345",
                name="",
                alternate_url="https://hh.ru/vacancy/12345",
                salary_from=100000,
                salary_to=150000,
                salary_currency="RUR",
                requirement="Python experience required",
            )

    def test_vacancy_salary_validation(self):
        """Тест валидации зарплаты"""
        vacancy = Vacancy(
            id="12345",
            name="Python Developer",
            alternate_url="https://hh.ru/vacancy/12345",
            salary_from=None,
            salary_to=-1000,
            salary_currency="RUR",
            requirement="Python experience required",
        )

        assert vacancy.salary_from == 0.0
        assert vacancy.salary_to == 0.0

    def test_vacancy_default_values(self):
        """Тест значений по умолчанию"""
        vacancy = Vacancy(
            id="12345",
            name="Python Developer",
            alternate_url="https://hh.ru/vacancy/12345",
            salary_from=100000,
            salary_to=150000,
            salary_currency=None,
            requirement="",
        )

        assert vacancy.salary_currency == "Не указана"
        assert vacancy.requirement == "Не указаны"

    def test_get_salary_average(self):
        """Тест вычисления средней зарплаты"""
        vacancy1 = Vacancy("1", "Dev", "url", 100000, 150000, "RUR", "req")
        assert vacancy1.get_salary_average() == 125000.0

        vacancy2 = Vacancy("2", "Dev", "url", 100000, 0, "RUR", "req")
        assert vacancy2.get_salary_average() == 100000.0

        vacancy3 = Vacancy("3", "Dev", "url", 0, 150000, "RUR", "req")
        assert vacancy3.get_salary_average() == 150000.0

        vacancy4 = Vacancy("4", "Dev", "url", 0, 0, "RUR", "req")
        assert vacancy4.get_salary_average() == 0.0

    def test_vacancy_comparison(self):
        """Тест методов сравнения вакансий"""
        vacancy1 = Vacancy("1", "Dev1", "url1", 100000, 150000, "RUR", "req1")  # avg: 125000
        vacancy2 = Vacancy("2", "Dev2", "url2", 200000, 250000, "RUR", "req2")  # avg: 225000
        vacancy3 = Vacancy("3", "Dev3", "url3", 100000, 150000, "RUR", "req3")  # avg: 125000

        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert vacancy1 <= vacancy2
        assert vacancy2 >= vacancy1
        assert vacancy1 <= vacancy3
        assert vacancy1 >= vacancy3

    def test_vacancy_equality(self):
        """Тест равенства вакансий"""
        vacancy1 = Vacancy("12345", "Dev1", "url1", 100000, 150000, "RUR", "req1")
        vacancy2 = Vacancy("12345", "Dev2", "url2", 200000, 250000, "USD", "req2")  # Тот же ID
        vacancy3 = Vacancy("67890", "Dev1", "url1", 100000, 150000, "RUR", "req1")  # Другой ID

        assert vacancy1 == vacancy2
        assert vacancy1 != vacancy3

    def test_vacancy_str_repr(self):
        """Тест строкового представления"""
        vacancy = Vacancy("12345", "Python Dev", "https://hh.ru/12345", 100000, 150000, "RUR", "Python req")

        str_repr = str(vacancy)
        assert "Python Dev" in str_repr
        assert "100000-150000 RUR" in str_repr
        assert "https://hh.ru/12345" in str_repr

        vacancy_no_salary = Vacancy("12346", "Java Dev", "https://hh.ru/12346", None, None, None, "Java req")
        str_no_salary = str(vacancy_no_salary)
        assert "Зарплата не указана" in str_no_salary

        vacancy_from = Vacancy("12347", "JS Dev", "https://hh.ru/12347", 80000, None, "RUR", "JS req")
        str_from = str(vacancy_from)
        assert "от 80000 RUR" in str_from

        vacancy_to = Vacancy("12348", "PHP Dev", "https://hh.ru/12348", None, 120000, "RUR", "PHP req")
        str_to = str(vacancy_to)
        assert "до 120000 RUR" in str_to

        repr_str = repr(vacancy)
        assert "Vacancy" in repr_str
        assert "12345" in repr_str
        assert "Python Dev" in repr_str

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy = Vacancy("12345", "Python Dev", "https://hh.ru/12345", 100000, 150000, "RUR", "Python req")

        result = vacancy.to_dict()

        expected = {
            "id": "12345",
            "name": "Python Dev",
            "alternate_url": "https://hh.ru/12345",
            "salary_from": 100000.0,
            "salary_to": 150000.0,
            "salary_currency": "RUR",
            "requirement": "Python req",
        }

        assert result == expected

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей в список объектов"""
        raw_data = [
            {
                "id": "12345",
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/12345",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Python experience"},
            },
            {
                "id": "67890",
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/67890",
                "salary": None,
                "snippet": {"requirement": "Java experience"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(raw_data)

        assert len(vacancies) == 2
        assert vacancies[0].id == "12345"
        assert vacancies[0].name == "Python Developer"
        assert vacancies[0].salary_from == 100000.0
        assert vacancies[0].salary_to == 150000.0

        assert vacancies[1].id == "67890"
        assert vacancies[1].salary_from == 0.0
        assert vacancies[1].salary_to == 0.0

    def test_cast_to_object_list_invalid_data(self):
        """Тест преобразования с невалидными данными"""
        raw_data = [
            {
                "id": "",
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/12345",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Python experience"},
            },
            {
                "id": "67890",
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/67890",
                "salary": {"from": 200000, "to": 250000, "currency": "RUR"},
                "snippet": {"requirement": "Java experience"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(raw_data)

        assert len(vacancies) == 1
        assert vacancies[0].id == "67890"
