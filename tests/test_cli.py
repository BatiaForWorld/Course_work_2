from unittest.mock import Mock, patch

from src.cli import user_interaction


class TestUserInteraction:
    """Тестирование основной функции пользовательского интерфейса"""

    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_user_interaction_exit_immediately(self, mock_print, mock_input):
        """Тест немедленного выхода из программы"""
        user_interaction()

        mock_print.assert_any_call("Добро пожаловать в программу поиска вакансий!")
        mock_print.assert_any_call("До свидания!")

    @patch("builtins.input", side_effect=["", "   ", "\t", "0"])
    @patch("builtins.print")
    def test_user_interaction_invalid_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода"""
        user_interaction()

        mock_print.assert_any_call("Пожалуйста, выберите один из вариантов (0-6).")

    @patch("builtins.input", side_effect=["abc", "1.5", "xyz", "0"])
    @patch("builtins.print")
    def test_user_interaction_invalid_non_digit_input(self, mock_print, mock_input):
        """Тест обработки нечислового ввода"""
        user_interaction()

        mock_print.assert_any_call("Пожалуйста, введите число от 0 до 6.")

    @patch("builtins.input", side_effect=["-1", "7", "10", "0"])
    @patch("builtins.print")
    def test_user_interaction_invalid_out_of_range_input(self, mock_print, mock_input):
        """Тест обработки ввода вне допустимого диапазона"""
        user_interaction()

        mock_print.assert_any_call("Нет такого варианта. Выберите число от 0 до 6.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["1", "python", "n", "0"])
    @patch("builtins.print")
    def test_user_interaction_search_option_empty_keyword(
        self, mock_print, mock_input, _mock_saver_class, _mock_hh_class
    ):
        """Тест выбора опции поиска с пустым ключевым словом"""
        with patch("builtins.input", side_effect=["1", "", "0"]):
            user_interaction()

        mock_print.assert_any_call("Поисковый запрос не может быть пустым.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("src.cli.Vacancy")
    @patch("builtins.input", side_effect=["1", "python", "n", "0"])
    @patch("builtins.print")
    def test_user_interaction_search_option_success(
        self, mock_print, mock_input, mock_vacancy, _mock_saver_class, _mock_hh_class, sample_vacancies
    ):
        """Тест успешного поиска вакансий"""
        mock_hh = Mock()
        mock_saver = Mock()
        _mock_hh_class.return_value = mock_hh
        _mock_saver_class.return_value = mock_saver

        raw_data = [v.to_dict() for v in sample_vacancies]
        mock_hh.load_vacancies.return_value = raw_data
        mock_vacancy.cast_to_object_list.return_value = sample_vacancies

        user_interaction()

        mock_hh.load_vacancies.assert_called_with("python")
        mock_print.assert_any_call("Поиск вакансий...")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["2", "", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_top_empty_input(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест показа топ вакансий с пустым вводом"""
        user_interaction()

        mock_print.assert_any_call("Количество не может быть пустым.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["2", "abc", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_top_non_digit(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест показа топ вакансий с нечисловым вводом"""
        user_interaction()

        mock_print.assert_any_call("Пожалуйста, введите положительное число.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["2", "0", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_top_zero_input(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест показа топ вакансий с нулевым количеством"""
        user_interaction()

        mock_print.assert_any_call("Количество должно быть положительным числом.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("src.cli.Vacancy")
    @patch("src.cli.sort_vacancies")
    @patch("src.cli.get_top_vacancies")
    @patch("src.cli.print_vacancies")
    @patch("builtins.input", side_effect=["2", "5", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_top_success(
        self,
        mock_print,
        mock_input,
        mock_print_vacancies,
        mock_get_top,
        mock_sort,
        mock_vacancy,
        _mock_saver_class,
        _mock_hh_class,
        sample_vacancies,
    ):
        """Тест успешного показа топ вакансий"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver

        raw_data = [v.to_dict() for v in sample_vacancies]
        mock_saver.get_all_vacancies.return_value = raw_data
        mock_vacancy.cast_to_object_list.return_value = sample_vacancies
        mock_sort.return_value = sample_vacancies
        mock_get_top.return_value = sample_vacancies[:2]

        user_interaction()

        mock_print_vacancies.assert_called_once()

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["3", "", "0"])
    @patch("builtins.print")
    def test_user_interaction_filter_keywords_empty(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест фильтрации по ключевым словам с пустым вводом"""
        user_interaction()

        mock_print.assert_any_call("Ключевые слова не могут быть пустыми.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("src.cli.Vacancy")
    @patch("src.cli.filter_vacancies")
    @patch("src.cli.print_vacancies")
    @patch("builtins.input", side_effect=["3", "python", "0"])
    @patch("builtins.print")
    def test_user_interaction_filter_keywords_success(
        self,
        mock_print,
        mock_input,
        mock_print_vacancies,
        mock_filter,
        mock_vacancy,
        _mock_saver_class,
        _mock_hh_class,
        sample_vacancies,
    ):
        """Тест успешной фильтрации по ключевым словам"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver

        raw_data = [v.to_dict() for v in sample_vacancies]
        mock_saver.get_all_vacancies.return_value = raw_data
        mock_vacancy.cast_to_object_list.return_value = sample_vacancies
        mock_filter.return_value = sample_vacancies

        user_interaction()

        mock_print_vacancies.assert_called_once()

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["4", "", "0"])
    @patch("builtins.print")
    def test_user_interaction_filter_salary_empty(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест фильтрации по зарплате с пустым вводом"""
        user_interaction()

        mock_print.assert_any_call("Диапазон зарплат не может быть пустым.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["4", "invalid", "0"])
    @patch("builtins.print")
    def test_user_interaction_filter_salary_invalid_format(
        self, mock_print, mock_input, _mock_saver_class, _mock_hh_class
    ):
        """Тест фильтрации по зарплате с некорректным форматом"""
        user_interaction()

        calls = [str(call) for call in mock_print.call_args_list]
        assert any("Ошибка в формате зарплаты" in call for call in calls)

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["5", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_all_no_data(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест показа всех вакансий без сохраненных данных"""

        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver
        mock_saver.get_all_vacancies.return_value = []

        user_interaction()

        mock_print.assert_any_call("Сохраненные вакансии не найдены.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("src.cli.Vacancy")
    @patch("src.cli.print_vacancies")
    @patch("builtins.input", side_effect=["5", "1", "0"])
    @patch("builtins.print")
    def test_user_interaction_show_all_success(
        self,
        mock_print,
        mock_input,
        mock_print_vacancies,
        mock_vacancy,
        _mock_saver_class,
        _mock_hh_class,
        sample_vacancies,
    ):
        """Тест успешного показа всех вакансий"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver

        raw_data = [v.to_dict() for v in sample_vacancies]
        mock_saver.get_all_vacancies.return_value = raw_data
        mock_vacancy.cast_to_object_list.return_value = sample_vacancies

        user_interaction()

        mock_print.assert_any_call("Всего сохранено 3 вакансий.")
        mock_print_vacancies.assert_called_once()

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["6", "", "0"])
    @patch("builtins.print")
    def test_user_interaction_delete_vacancy_empty_id(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест удаления вакансии с пустым ID"""
        user_interaction()

        mock_print.assert_any_call("ID вакансии не может быть пустым.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["6", "12345", "0"])
    @patch("builtins.print")
    def test_user_interaction_delete_vacancy_success(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест успешного удаления вакансии"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver

        user_interaction()

        mock_saver.delete_vacancy.assert_called_once_with("12345")
        mock_print.assert_any_call("Вакансия с ID 12345 удалена.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["6", "99999", "0"])
    @patch("builtins.print")
    def test_user_interaction_delete_vacancy_error(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест обработки ошибки при удалении вакансии"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver
        mock_saver.delete_vacancy.side_effect = Exception("Vacancy not found")

        user_interaction()

        mock_print.assert_any_call("Ошибка при удалении: Vacancy not found")


class TestComplexScenarios:
    """Тестирование сложных сценариев использования CLI"""

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["3", "   ", "0"])
    @patch("builtins.print")
    def test_filter_keywords_whitespace_only(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест фильтрации с пробелами"""
        user_interaction()

        mock_print.assert_any_call("Ключевые слова не могут быть пустыми.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["2", "-5", "0"])
    @patch("builtins.print")
    def test_show_top_negative_number(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест с отрицательным числом для топа"""
        user_interaction()

        mock_print.assert_any_call("Пожалуйста, введите положительное число.")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["4", "abc-def", "0"])
    @patch("builtins.print")
    def test_salary_filter_invalid_range(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест с некорректным диапазоном зарплат"""
        user_interaction()

        calls = [str(call) for call in mock_print.call_args_list]
        assert any("Ошибка в формате зарплаты" in call for call in calls)

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["1", "test", "n", "1", "python", "y", "0"])
    @patch("builtins.print")
    def test_multiple_operations_sequence(
        self, mock_print, mock_input, _mock_saver_class, _mock_hh_class, sample_vacancies
    ):
        """Тест последовательности операций"""
        mock_hh = Mock()
        mock_saver = Mock()
        _mock_hh_class.return_value = mock_hh
        _mock_saver_class.return_value = mock_saver

        raw_data = [v.to_dict() for v in sample_vacancies]
        mock_hh.load_vacancies.return_value = raw_data

        with patch("src.cli.Vacancy") as mock_vacancy:
            mock_vacancy.cast_to_object_list.return_value = sample_vacancies
            with patch("src.cli.print_vacancies"):
                user_interaction()

        assert mock_hh.load_vacancies.call_count == 2
        mock_hh.load_vacancies.assert_any_call("test")
        mock_hh.load_vacancies.assert_any_call("python")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("builtins.input", side_effect=["1", "error_test", "0"])
    @patch("builtins.print")
    def test_api_error_handling(self, mock_print, mock_input, _mock_saver_class, _mock_hh_class):
        """Тест обработки ошибок API"""
        mock_hh = Mock()
        _mock_hh_class.return_value = mock_hh
        mock_hh.load_vacancies.side_effect = Exception("API Error")

        user_interaction()

        mock_print.assert_any_call("Ошибка при поиске вакансий: API Error")

    @patch("src.cli.HH")
    @patch("src.cli.JSONSaver")
    @patch("src.cli.Vacancy")
    @patch("builtins.input", side_effect=["5", "2", "0"])
    @patch("builtins.print")
    def test_show_all_with_salary_filter(
        self, mock_print, mock_input, mock_vacancy, _mock_saver_class, _mock_hh_class, complex_vacancy_scenarios
    ):
        """Тест показа только вакансий с зарплатой"""
        mock_saver = Mock()
        _mock_saver_class.return_value = mock_saver

        mixed_vacancies = complex_vacancy_scenarios["mixed_salary_vacancies"]
        raw_data = [v.to_dict() for v in mixed_vacancies]
        mock_saver.get_all_vacancies.return_value = raw_data
        mock_vacancy.cast_to_object_list.return_value = mixed_vacancies

        with patch("src.cli.print_vacancies") as mock_print_vacancies:
            user_interaction()
            mock_print_vacancies.assert_called_once()
