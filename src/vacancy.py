from typing import Any, Dict, List, Optional, Union


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    __slots__ = ("id", "name", "alternate_url", "salary_from", "salary_to", "salary_currency", "requirement")

    def __init__(
        self,
        id: str,
        name: str,
        alternate_url: str,
        salary_from: Optional[Union[int, float]],
        salary_to: Optional[Union[int, float]],
        salary_currency: Optional[str],
        requirement: str,
    ):
        """
        Инициализация вакансии
        """
        self.id = self._validate_string(id, "ID")
        self.name = self._validate_string(name, "Name")
        self.alternate_url = self._validate_string(alternate_url, "URL")
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.salary_currency = salary_currency or "Не указана"
        self.requirement = requirement or "Не указаны"

    def _validate_string(self, value: Any, field_name: str) -> str:
        """
        Приватный метод валидации строковых полей
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} должно быть непустой строкой")
        return value.strip()

    def _validate_salary(self, value: Optional[Union[int, float]]) -> float:
        """
        Приватный метод валидации зарплаты
        """
        if value is None:
            return 0.0
        if not isinstance(value, (int, float)) or value < 0:
            return 0.0
        return float(value)

    def get_salary_average(self) -> float:
        """
        Вычисление средней зарплаты
        """
        if self.salary_from > 0 and self.salary_to > 0:
            return (self.salary_from + self.salary_to) / 2
        return self.salary_from or self.salary_to or 0.0

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий (меньше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_average() < other.get_salary_average()

    def __le__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий (меньше или равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_average() <= other.get_salary_average()

    def __gt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий (больше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_average() > other.get_salary_average()

    def __ge__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий (больше или равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary_average() >= other.get_salary_average()

    def __eq__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий (равенство)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.id == other.id

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        if self.salary_from == 0.0 and self.salary_to == 0.0:
            salary_str = "Зарплата не указана"
        elif self.salary_from > 0 and self.salary_to > 0:
            salary_str = f"{int(self.salary_from)}-{int(self.salary_to)} {self.salary_currency}"
        elif self.salary_from > 0:
            salary_str = f"от {int(self.salary_from)} {self.salary_currency}"
        elif self.salary_to > 0:
            salary_str = f"до {int(self.salary_to)} {self.salary_currency}"
        else:
            salary_str = "Зарплата не указана"

        return f"{self.name} | {salary_str} | {self.alternate_url}"

    def __repr__(self) -> str:
        """Представление вакансии для разработчика"""
        return f"Vacancy(id='{self.id}', name='{self.name}', salary={self.get_salary_average()})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование вакансии в словарь
        """
        return {
            "id": self.id,
            "name": self.name,
            "alternate_url": self.alternate_url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "salary_currency": self.salary_currency,
            "requirement": self.requirement,
        }

    @classmethod
    def cast_to_object_list(cls, raw_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """
        Преобразование списка словарей в список объектов Vacancy
        """
        vacancies = []
        for item in raw_data:
            try:

                if "salary_from" in item:
                    salary_from = item.get("salary_from")
                    salary_to = item.get("salary_to")
                    salary_currency = item.get("salary_currency")
                else:
                    salary = item.get("salary", {}) or {}
                    salary_from = salary.get("from") if isinstance(salary, dict) else None
                    salary_to = salary.get("to") if isinstance(salary, dict) else None
                    salary_currency = salary.get("currency") if isinstance(salary, dict) else None

                vacancies.append(
                    cls(
                        id=item.get("id", ""),
                        name=item.get("name", ""),
                        alternate_url=item.get("alternate_url", ""),
                        salary_from=salary_from,
                        salary_to=salary_to,
                        salary_currency=salary_currency,
                        requirement=(
                            item.get("snippet", {}).get("requirement", "")
                            if isinstance(item.get("snippet"), dict)
                            else item.get("requirement", "")
                        ),
                    )
                )
            except (ValueError, KeyError):
                continue
        return vacancies
