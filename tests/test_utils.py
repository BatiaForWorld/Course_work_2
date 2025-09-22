from unittest.mock import patch

import pytest

from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    parse_salary_range,
    print_vacancies,
    sort_vacancies,
)
from src.vacancy import Vacancy


class TestUtils:
    """Тесты для модуля utils"""

    @pytest.fixture
    def sample_vacancies(self):
        """Фикстура с примерами вакансий"""
        return [
            Vacancy("1", "Python Developer", "url1", 100000, 150000, "RUR", "Python experience"),
            Vacancy("2", "Java Developer", "url2", 120000, 180000, "RUR", "Java experience"),
            Vacancy("3", "Python Senior", "url3", 200000, 250000, "RUR", "Senior Python developer"),
            Vacancy("4", "Frontend Developer", "url4", 80000, 120000, "RUR", "JavaScript React"),
        ]

    def test_filter_vacancies(self, sample_vacancies):
        """Тест фильтрации вакансий по ключевым словам"""
        result = filter_vacancies(sample_vacancies, ["Python"])

        assert len(result) == 2
        assert result[0].id == "1"
        assert result[1].id == "3"

    def test_filter_vacancies_multiple_words(self, sample_vacancies):
        """Тест фильтрации по нескольким ключевым словам"""
        result = filter_vacancies(sample_vacancies, ["Python", "Senior"])

        assert len(result) == 1
        assert result[0].id == "3"

    def test_filter_vacancies_no_matches(self, sample_vacancies):
        """Тест фильтрации без совпадений"""
        result = filter_vacancies(sample_vacancies, ["C++"])

        assert len(result) == 0

    def test_get_vacancies_by_salary(self, sample_vacancies):
        """Тест фильтрации по диапазону зарплат"""
        result = get_vacancies_by_salary(sample_vacancies, (100000, 160000))

        assert len(result) == 3
        vacancy_ids = [v.id for v in result]
        assert "1" in vacancy_ids
        assert "2" in vacancy_ids
        assert "4" in vacancy_ids

    def test_get_vacancies_by_salary_high_range(self, sample_vacancies):
        """Тест фильтрации по высокому диапазону зарплат"""
        result = get_vacancies_by_salary(sample_vacancies, (200000, 300000))

        assert len(result) == 1
        assert result[0].id == "3"

    def test_sort_vacancies_descending(self, sample_vacancies):
        """Тест сортировки вакансий по убыванию зарплаты"""
        result = sort_vacancies(sample_vacancies)

        assert result[0].id == "3"
        assert result[1].id == "2"
        assert result[2].id == "1"
        assert result[3].id == "4"

    def test_sort_vacancies_ascending(self, sample_vacancies):
        """Тест сортировки вакансий по возрастанию зарплаты"""
        result = sort_vacancies(sample_vacancies, reverse=False)

        assert result[0].id == "4"
        assert result[1].id == "1"
        assert result[2].id == "2"
        assert result[3].id == "3"

    def test_get_top_vacancies(self, sample_vacancies):
        """Тест получения топ N вакансий"""
        sorted_vacancies = sort_vacancies(sample_vacancies)
        result = get_top_vacancies(sorted_vacancies, 2)

        assert len(result) == 2
        assert result[0].id == "3"
        assert result[1].id == "2"

    def test_get_top_vacancies_more_than_available(self, sample_vacancies):
        """Тест получения топа больше, чем есть вакансий"""
        result = get_top_vacancies(sample_vacancies, 10)

        assert len(result) == 4

    def test_get_top_vacancies_zero(self, sample_vacancies):
        """Тест получения топа с нулевым количеством"""
        result = get_top_vacancies(sample_vacancies, 0)

        assert len(result) == 0

    @patch("builtins.print")
    def test_print_vacancies(self, mock_print, sample_vacancies):
        """Тест печати вакансий"""
        print_vacancies(sample_vacancies[:2])

        assert mock_print.call_count > 0

    @patch("builtins.print")
    def test_print_vacancies_empty(self, mock_print):
        """Тест печати пустого списка вакансий"""
        print_vacancies([])

        mock_print.assert_called_with("Вакансии не найдены.")

    def test_parse_salary_range_valid(self):
        """Тест парсинга валидного диапазона зарплат"""
        result = parse_salary_range("100000-150000")
        assert result == (100000.0, 150000.0)

        result = parse_salary_range("100000 - 150000")
        assert result == (100000.0, 150000.0)

    def test_parse_salary_range_reversed(self):
        """Тест парсинга обращенного диапазона"""
        result = parse_salary_range("150000-100000")
        assert result == (100000.0, 150000.0)

    def test_parse_salary_range_invalid_format(self):
        """Тест парсинга невалидного формата"""
        with pytest.raises(ValueError, match="Неверный формат диапазона зарплат"):
            parse_salary_range("100000")

        with pytest.raises(ValueError, match="Неверный формат диапазона зарплат"):
            parse_salary_range("100000-150000-200000")

    def test_parse_salary_range_negative(self):
        """Тест парсинга с отрицательными значениями"""
        with pytest.raises(ValueError, match="Зарплата не может быть отрицательной"):
            parse_salary_range("-100000-150000")

    def test_parse_salary_range_non_numeric(self):
        """Тест парсинга с нечисловыми значениями"""
        with pytest.raises(ValueError, match="Зарплата должна быть числом"):
            parse_salary_range("abc-150000")
