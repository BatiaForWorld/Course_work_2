from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class FileHandler(ABC):
    """
    Абстрактный класс для работы с файлами вакансий
    """

    @abstractmethod
    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """
        Абстрактный метод добавления вакансии в файл
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Абстрактный метод удаления вакансии из файла по ID
        """
        pass

    @abstractmethod
    def filter_vacancies(self, filter_words: List[str]) -> List[Dict[str, Any]]:
        """
        Абстрактный метод фильтрации вакансий по ключевым словам
        """
        pass

    @abstractmethod
    def filter_vacancies_by_salary(self, salary_range: Tuple[float, float]) -> List[Dict[str, Any]]:
        """
        Абстрактный метод фильтрации вакансий по диапазону зарплат
        """
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Абстрактный метод получения всех вакансий из файла
        """
        pass
