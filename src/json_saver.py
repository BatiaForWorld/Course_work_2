import json
import os
from typing import Any, Dict, List, Tuple

from .file_handler import FileHandler


class JSONSaver(FileHandler):
    """
    Класс для сохранения вакансий в JSON-файл
    """

    def __init__(self, filename: str = "data/vacancies.json"):
        """
        Инициализация сохранителя JSON
        """
        # Создаем папку только если есть путь к директории
        dirname = os.path.dirname(filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        self.__filename = filename
        if not os.path.exists(self.__filename):
            self._create_empty_file()

    def _create_empty_file(self) -> None:
        """
        Приватный метод создания пустого файла
        """
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=2)

    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Приватный метод загрузки данных из файла
        """
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Приватный метод сохранения данных в файл
        """
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """
        Добавление вакансии в файл (без дубликатов)
        """
        vacancies = self._load_data()

        vacancy_id = vacancy_data.get("id")
        if vacancy_id and not any(v.get("id") == vacancy_id for v in vacancies):
            vacancies.append(vacancy_data)
            self._save_data(vacancies)

    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Удаление вакансии из файла по ID
        """
        vacancies = self._load_data()
        filtered_vacancies = [v for v in vacancies if v.get("id") != vacancy_id]
        self._save_data(filtered_vacancies)

    def filter_vacancies(self, filter_words: List[str]) -> List[Dict[str, Any]]:
        """
        Фильтрация вакансий по ключевым словам
        """
        vacancies = self._load_data()
        filtered = []

        for vacancy in vacancies:
            name = vacancy.get("name", "").lower()
            requirement = vacancy.get("requirement", "").lower()
            search_text = f"{name} {requirement}"

            if all(word.lower() in search_text for word in filter_words):
                filtered.append(vacancy)

        return filtered

    def filter_vacancies_by_salary(self, salary_range: Tuple[float, float]) -> List[Dict[str, Any]]:
        """
        Фильтрация вакансий по диапазону зарплат
        """
        vacancies = self._load_data()
        min_salary, max_salary = salary_range
        filtered = []

        for vacancy in vacancies:
            salary_from = vacancy.get("salary_from", 0) or 0
            salary_to = vacancy.get("salary_to", 0) or 0

            avg_salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to

            if min_salary <= avg_salary <= max_salary:
                filtered.append(vacancy)

        return filtered

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получение всех вакансий из файла
        """
        return self._load_data()
