from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Parser(ABC):
    """
    Абстрактный класс для парсеров вакансий
    """

    def __init__(self, file_worker):
        """
        Инициализация парсера с файловым обработчиком
        """
        self.file_worker = file_worker

    @abstractmethod
    def _connect(self) -> None:
        """
        Приватный метод подключения к API (абстрактный)
        """
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Абстрактный метод для загрузки вакансий
        """
        pass
