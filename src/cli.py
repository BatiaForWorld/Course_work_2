from .hh import HH
from .json_saver import JSONSaver
from .utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    parse_salary_range,
    print_vacancies,
    sort_vacancies,
)
from .vacancy import Vacancy


def user_interaction() -> None:
    """
    Функция взаимодействия с пользователем через консоль
    """
    print("Добро пожаловать в программу поиска вакансий!")
    print("=" * 50)

    json_saver = JSONSaver()
    hh_api = HH(json_saver)

    while True:
        print("\nВыберите действие:")
        print("1. Найти вакансии на HeadHunter")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Фильтровать вакансии по ключевым словам")
        print("4. Фильтровать вакансии по диапазону зарплат")
        print("5. Показать все сохраненные вакансии")
        print("6. Удалить вакансию по ID")
        print("0. Выход")

        choice = input("\nВаш выбор: ").strip()

        if not choice:
            print("Пожалуйста, выберите один из вариантов (0-6).")
            continue

        if not choice.isdigit():
            print("Пожалуйста, введите число от 0 до 6.")
            continue

        choice_num = int(choice)

        if choice_num < 0 or choice_num > 6:
            print("Нет такого варианта. Выберите число от 0 до 6.")
            continue

        if choice_num == 1:
            _search_vacancies(hh_api, json_saver)
        elif choice_num == 2:
            _show_top_vacancies(json_saver)
        elif choice_num == 3:
            _filter_by_keywords(json_saver)
        elif choice_num == 4:
            _filter_by_salary(json_saver)
        elif choice_num == 5:
            _show_all_vacancies(json_saver)
        elif choice_num == 6:
            _delete_vacancy(json_saver)
        elif choice_num == 0:
            print("До свидания!")
            break


def _search_vacancies(hh_api: HH, json_saver: JSONSaver) -> None:
    """
    Поиск и сохранение вакансий
    """
    keyword = input("Введите поисковый запрос: ").strip()
    if not keyword:
        print("Поисковый запрос не может быть пустым.")
        return

    try:
        print("Поиск вакансий...")
        raw_vacancies = hh_api.load_vacancies(keyword)

        if not raw_vacancies:
            print("Вакансии не найдены.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)

        with_salary = [v for v in vacancies if v.salary_from > 0 or v.salary_to > 0]
        print(f"Найдено {len(vacancies)} вакансий (из них {len(with_salary)} с указанной зарплатой).")

        for vacancy in vacancies:
            json_saver.add_vacancy(vacancy.to_dict())

        print(f"Все вакансии сохранены в файл {json_saver._JSONSaver__filename}.")

        show_results = input("Показать найденные вакансии? (y/n): ").strip().lower()
        if show_results == "y":
            print_vacancies(vacancies)

    except Exception as e:
        print(f"Ошибка при поиске вакансий: {e}")


def _show_top_vacancies(json_saver: JSONSaver) -> None:
    """
    Показ топ N вакансий по зарплате
    """
    try:
        n_input = input("Введите количество вакансий для топа: ").strip()

        if not n_input:
            print("Количество не может быть пустым.")
            return

        if not n_input.isdigit():
            print("Пожалуйста, введите положительное число.")
            return

        n = int(n_input)
        if n <= 0:
            print("Количество должно быть положительным числом.")
            return

        raw_vacancies = json_saver.get_all_vacancies()
        if not raw_vacancies:
            print("Сохраненные вакансии не найдены.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)
        sorted_vacancies = sort_vacancies(vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, n)

        print_vacancies(top_vacancies)

    except ValueError:
        print("Некорректное число.")
    except Exception as e:
        print(f"Ошибка: {e}")


def _filter_by_keywords(json_saver: JSONSaver) -> None:
    """
    Фильтрация по ключевым словам
    """
    keywords_str = input("Введите ключевые слова через пробел: ").strip()
    if not keywords_str:
        print("Ключевые слова не могут быть пустыми.")
        return

    keywords = keywords_str.split()

    try:
        raw_vacancies = json_saver.get_all_vacancies()
        if not raw_vacancies:
            print("Сохраненные вакансии не найдены.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)
        filtered_vacancies = filter_vacancies(vacancies, keywords)

        print_vacancies(filtered_vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _filter_by_salary(json_saver: JSONSaver) -> None:
    """
    Фильтрация по диапазону зарплат
    """
    salary_str = input("Введите диапазон зарплат (например, 100000-150000): ").strip()
    if not salary_str:
        print("Диапазон зарплат не может быть пустым.")
        return

    try:
        salary_range = parse_salary_range(salary_str)

        raw_vacancies = json_saver.get_all_vacancies()
        if not raw_vacancies:
            print("Сохраненные вакансии не найдены.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)
        filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)

        print_vacancies(filtered_vacancies)

    except ValueError as e:
        print(f"Ошибка в формате зарплаты: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


def _show_all_vacancies(json_saver: JSONSaver) -> None:
    """
    Показ всех сохраненных вакансий
    """
    try:
        raw_vacancies = json_saver.get_all_vacancies()
        if not raw_vacancies:
            print("Сохраненные вакансии не найдены.")
            return

        vacancies = Vacancy.cast_to_object_list(raw_vacancies)

        print(f"Всего сохранено {len(vacancies)} вакансий.")

        filter_choice = input("Показать: 1 - Все вакансии, 2 - Только с указанной зарплатой: ").strip()

        if filter_choice == "2":
            vacancies_with_salary = [v for v in vacancies if v.salary_from > 0 or v.salary_to > 0]
            if vacancies_with_salary:
                print(f"Найдено {len(vacancies_with_salary)} вакансий с указанной зарплатой:")
                print_vacancies(vacancies_with_salary)
            else:
                print("Вакансии с указанной зарплатой не найдены.")
        else:
            print_vacancies(vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _delete_vacancy(json_saver: JSONSaver) -> None:
    """
    Удаление вакансии по ID
    """
    vacancy_id = input("Введите ID вакансии для удаления: ").strip()
    if not vacancy_id:
        print("ID вакансии не может быть пустым.")
        return

    try:
        json_saver.delete_vacancy(vacancy_id)
        print(f"Вакансия с ID {vacancy_id} удалена.")

    except Exception as e:
        print(f"Ошибка при удалении: {e}")
