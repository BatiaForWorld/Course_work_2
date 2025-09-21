from typing import List, Tuple

from .vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам
    """
    filtered = []
    for vacancy in vacancies:
        search_text = f"{vacancy.name} {vacancy.requirement}".lower()
        if all(word.lower() in search_text for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: Tuple[float, float]) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат
    """
    min_salary, max_salary = salary_range
    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.get_salary_average()
        if min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """
    Сортировка вакансий по средней зарплате
    """
    return sorted(vacancies, key=lambda x: x.get_salary_average(), reverse=reverse)


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий
    """
    return vacancies[:n] if n > 0 else []


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Печать вакансий в человекочитаемом виде
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"\nНайдено вакансий: {len(vacancies)}")
    print("-" * 80)

    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")
        if vacancy.requirement and vacancy.requirement != "Не указаны":
            print(f"   Требования: {vacancy.requirement[:100]}...")
        print()


def parse_salary_range(salary_input: str) -> Tuple[float, float]:
    """
    Парсинг строки диапазона зарплат
    """
    try:
        salary_input = salary_input.replace(" ", "")
        if "-" not in salary_input:
            raise ValueError("Неверный формат диапазона зарплат")

        dash_count = salary_input.count("-")

        if dash_count > 2:  # Слишком много дефисов
            raise ValueError("Неверный формат диапазона зарплат")

        if dash_count == 1:
            dash_pos = salary_input.find("-")
            if dash_pos == 0 or dash_pos == len(salary_input) - 1:
                raise ValueError("Неверный формат диапазона зарплат")
            parts = [salary_input[:dash_pos], salary_input[dash_pos + 1 :]]

        elif dash_count == 2:
            if salary_input.startswith("-"):

                next_dash_pos = salary_input.find("-", 1)
                if next_dash_pos == -1:
                    raise ValueError("Неверный формат диапазона зарплат")
                parts = [salary_input[:next_dash_pos], salary_input[next_dash_pos + 1 :]]
            else:

                first_dash_pos = salary_input.find("-")
                second_dash_pos = salary_input.find("-", first_dash_pos + 1)

                if second_dash_pos != first_dash_pos + 1:
                    raise ValueError("Неверный формат диапазона зарплат")

                remaining_part = salary_input[second_dash_pos + 1 :]
                parts = [salary_input[:first_dash_pos], "-" + remaining_part]

        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("Неверный формат диапазона зарплат")

        min_salary = float(parts[0])
        max_salary = float(parts[1])

        if min_salary < 0 or max_salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

        if min_salary > max_salary:
            min_salary, max_salary = max_salary, min_salary

        return min_salary, max_salary

    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError("Зарплата должна быть числом")
        raise
