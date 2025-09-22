import json
from unittest.mock import mock_open, patch

from src.json_saver import JSONSaver


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def test_json_saver_init_default(self):
        """Тест инициализации с файлом по умолчанию"""
        with patch("os.path.exists", return_value=False):
            with patch("os.makedirs") as mock_makedirs:
                with patch("builtins.open", mock_open()) as mock_file:
                    with patch("json.dump") as mock_json_dump:
                        saver = JSONSaver()

                        assert saver._JSONSaver__filename == "data/vacancies.json"
                        mock_makedirs.assert_called_once_with("data", exist_ok=True)
                        mock_file.assert_called_once_with("data/vacancies.json", "w", encoding="utf-8")
                        mock_json_dump.assert_called_once_with(
                            [], mock_file.return_value, ensure_ascii=False, indent=2
                        )

    def test_json_saver_init_custom_filename(self):
        """Тест инициализации с пользовательским файлом"""
        with patch("os.path.exists", return_value=False):
            with patch("builtins.open", mock_open()) as mock_file:
                with patch("json.dump") as mock_json_dump:
                    saver = JSONSaver("test_vacancies.json")

                    assert saver._JSONSaver__filename == "test_vacancies.json"
                    mock_file.assert_called_once_with("test_vacancies.json", "w", encoding="utf-8")

    def test_load_data_existing_file(self):
        """Тест загрузки данных из существующего файла"""
        test_data = [{"id": "123", "name": "Test Vacancy"}]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            saver = JSONSaver("test.json")
            result = saver._load_data()

            assert result == test_data

    def test_load_data_file_not_found(self):
        """Тест загрузки данных из несуществующего файла"""
        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch("builtins.open", side_effect=FileNotFoundError):
                result = saver._load_data()
                assert result == []

    def test_load_data_json_decode_error(self):
        """Тест обработки ошибки JSON декодирования"""
        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch("builtins.open", mock_open(read_data="invalid json")):
                result = saver._load_data()
                assert result == []

    def test_save_data(self):
        """Тест сохранения данных в файл"""
        test_data = [{"id": "123", "name": "Test Vacancy"}]

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch("builtins.open", mock_open()) as mock_file:
                with patch("json.dump") as mock_json_dump:
                    saver._save_data(test_data)

                    mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")
                    mock_json_dump.assert_called_once_with(
                        test_data, mock_file.return_value, ensure_ascii=False, indent=2
                    )

    def test_add_vacancy_new(self):
        """Тест добавления новой вакансии"""
        existing_data = []
        vacancy_data = {"id": "123", "name": "New Vacancy"}

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=existing_data):
                with patch.object(saver, "_save_data") as mock_save:
                    saver.add_vacancy(vacancy_data)

                    mock_save.assert_called_once_with([vacancy_data])

    def test_add_vacancy_duplicate(self):
        """Тест попытки добавления дублирующейся вакансии"""
        existing_data = [{"id": "123", "name": "Existing Vacancy"}]
        vacancy_data = {"id": "123", "name": "Duplicate Vacancy"}

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=existing_data):
                with patch.object(saver, "_save_data") as mock_save:
                    saver.add_vacancy(vacancy_data)

                    # Не должно вызываться, так как вакансия уже существует
                    mock_save.assert_not_called()

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        existing_data = [{"id": "123", "name": "To Delete"}, {"id": "456", "name": "To Keep"}]

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=existing_data):
                with patch.object(saver, "_save_data") as mock_save:
                    saver.delete_vacancy("123")

                    expected_data = [{"id": "456", "name": "To Keep"}]
                    mock_save.assert_called_once_with(expected_data)

    def test_filter_vacancies(self):
        """Тест фильтрации вакансий по ключевым словам"""
        existing_data = [
            {"id": "1", "name": "Python Developer", "requirement": "Python experience"},
            {"id": "2", "name": "Java Developer", "requirement": "Java experience"},
            {"id": "3", "name": "Python Senior", "requirement": "Senior Python"},
        ]

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=existing_data):
                result = saver.filter_vacancies(["Python"])

                assert len(result) == 2
                assert result[0]["id"] == "1"
                assert result[1]["id"] == "3"

    def test_filter_vacancies_by_salary(self):
        """Тест фильтрации вакансий по диапазону зарплат"""
        existing_data = [
            {"id": "1", "salary_from": 100000, "salary_to": 150000},  # avg: 125000
            {"id": "2", "salary_from": 200000, "salary_to": 250000},  # avg: 225000
            {"id": "3", "salary_from": 80000, "salary_to": 0},  # avg: 80000
        ]

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=existing_data):
                result = saver.filter_vacancies_by_salary((100000, 200000))

                assert len(result) == 1
                assert result[0]["id"] == "1"

    def test_get_all_vacancies(self):
        """Тест получения всех вакансий"""
        test_data = [{"id": "123", "name": "Test Vacancy"}]

        with patch("os.path.exists", return_value=True):
            saver = JSONSaver("test.json")

            with patch.object(saver, "_load_data", return_value=test_data) as mock_load:
                result = saver.get_all_vacancies()

                assert result == test_data
                mock_load.assert_called_once()
