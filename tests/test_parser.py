from abc import ABC

import pytest

from src.json_saver import JSONSaver
from src.parser import Parser


class TestParser:
    """Тесты для абстрактного класса Parser"""

    def test_parser_is_abstract(self):
        """Тест что Parser является абстрактным классом"""
        assert issubclass(Parser, ABC)

    def test_parser_cannot_be_instantiated(self):
        """Тест что Parser нельзя инстанцировать напрямую"""
        json_saver = JSONSaver("test.json")

        with pytest.raises(TypeError):
            Parser(json_saver)

    def test_parser_abstract_methods(self):
        """Тест наличия абстрактных методов"""
        assert hasattr(Parser, "_connect")
        assert hasattr(Parser, "load_vacancies")

        assert getattr(Parser._connect, "__isabstractmethod__", False)
        assert getattr(Parser.load_vacancies, "__isabstractmethod__", False)

    def test_concrete_parser_implementation(self):
        """Тест что конкретная реализация Parser работает"""
        json_saver = JSONSaver("test.json")

        class ConcreteParser(Parser):
            def _connect(self):
                return "connected"

            def load_vacancies(self, keyword):
                return [{"id": "1", "name": f"Vacancy for {keyword}"}]

        parser = ConcreteParser(json_saver)

        assert parser.file_worker == json_saver
        assert parser._connect() == "connected"
        assert parser.load_vacancies("Python") == [{"id": "1", "name": "Vacancy for Python"}]

    def test_parser_init(self):
        """Тест инициализации Parser с file_worker"""
        json_saver = JSONSaver("test.json")

        class ConcreteParser(Parser):
            def _connect(self):
                pass

            def load_vacancies(self, keyword):
                return []

        parser = ConcreteParser(json_saver)

        assert parser.file_worker == json_saver
