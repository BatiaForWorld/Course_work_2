from unittest.mock import Mock, patch

import pytest

from src.hh import HH
from src.json_saver import JSONSaver


class TestHH:
    """Тесты для класса HH"""

    def test_hh_init(self):
        """Тест инициализации класса HH"""
        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        assert hh.file_worker == json_saver
        assert hasattr(hh, "_HH__url")
        assert hasattr(hh, "_HH__headers")
        assert hasattr(hh, "_HH__params")
        assert hasattr(hh, "_HH__vacancies")

    @patch("requests.get")
    def test_connect_success(self, mock_get):
        """Тест успешного подключения к API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        hh._connect()
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_connect_failure(self, mock_get):
        """Тест неудачного подключения к API"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        with pytest.raises(ConnectionError):
            hh._connect()

    @patch("requests.get")
    def test_load_vacancies_success(self, mock_get):
        """Тест успешной загрузки вакансий"""
        mock_connect_response = Mock()
        mock_connect_response.status_code = 200

        mock_load_response = Mock()
        mock_load_response.status_code = 200
        mock_load_response.json.return_value = {
            "items": [
                {
                    "id": "12345",
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/12345",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {"requirement": "Python experience"},
                }
            ]
        }

        mock_empty_response = Mock()
        mock_empty_response.status_code = 200
        mock_empty_response.json.return_value = {"items": []}

        mock_get.side_effect = [mock_connect_response, mock_load_response, mock_empty_response]

        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        result = hh.load_vacancies("Python")

        assert len(result) == 1
        assert result[0]["id"] == "12345"
        assert result[0]["name"] == "Python Developer"

    @patch("requests.get")
    def test_load_vacancies_connection_error(self, mock_get):
        """Тест обработки ошибки подключения при загрузке вакансий"""
        mock_get.side_effect = Exception("Connection error")

        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        with pytest.raises(ConnectionError):
            hh.load_vacancies("Python")

    @patch("requests.get")
    def test_load_vacancies_empty_result(self, mock_get):
        """Тест загрузки пустого результата"""
        mock_connect_response = Mock()
        mock_connect_response.status_code = 200

        mock_load_response = Mock()
        mock_load_response.status_code = 200
        mock_load_response.json.return_value = {"items": []}

        mock_get.side_effect = [mock_connect_response, mock_load_response]

        json_saver = JSONSaver("test.json")
        hh = HH(json_saver)

        result = hh.load_vacancies("Python")

        assert len(result) == 0
