# Поиск вакансий с HeadHunter API

Курсовая работа по ООП: приложение для поиска, сохранения и управления вакансиями с платформы HeadHunter.ru с использованием официального API.

## Описание проекта

Консольное приложение для работы с вакансиями HeadHunter, реализующее:
- Интеграцию с API hh.ru
- Объектно-ориентированную архитектуру  
- Валидацию и сериализацию данных
- Фильтрацию и сортировку вакансий
- Персистентное хранение в JSON
- Полное тестовое покрытие с использованием pytest



## Требования

- Python 3.12+
- Poetry для управления зависимостями
- Интернет-соединение для работы с API

## Установка и запуск

### С Poetry (рекомендуется)

1. Клонируйте репозиторий:
```bash
https://github.com/BatiaForWorld/Course_work_2.git

```

2. Установите Poetry (если еще не установлен):
```bash
pip install poetry
```

3. Установите зависимостей через Poetry:
```bash
poetry add --group dev pytest flake8 pytest--cov
poetry sdd --group lint isort black mypy
poetry sdd dotenv
```

4. Запустите приложение через Poetry:
```bash
poetry run python3 main.py
```


## Функциональность

### Основные возможности:
- Поиск вакансий по ключевым словам через API hh.ru
- Сохранение найденных вакансий в JSON файл
- Просмотр всех сохраненных вакансий
- Получение топ N вакансий по зарплате
- Фильтрация вакансий по ключевым словам в названии и описании
- Фильтрация вакансий по диапазону зарплат
- Удаление вакансий из хранилища по ID

### Консольное меню:
```
1. Загрузить новые вакансии с hh.ru
2. Показать топ N вакансий по зарплате
3. Фильтровать вакансии по ключевым словам
4. Фильтровать вакансии по диапазону зарплат
5. Показать все вакансии
6. Удалить вакансию по id
0. Выход
```

## Архитектура

### Принципы ООП:
- **Наследование**: Абстрактные классы `VacancyAPI` и `FileHandler`
- **Инкапсуляция**: Приватные атрибуты (двойное подчеркивание)
- **Полиморфизм**: Магические методы сравнения в `Vacancy`
- **Абстракция**: Интерфейсы для API и хранилища данных

### Паттерны проектирования:
- **Strategy**: Разные реализации API (HeadHunter, можно добавить другие)
- **Template Method**: Базовые классы с абстрактными методами
- **Data Transfer Object**: Класс `Vacancy` для передачи данных

## Ключевые классы

### Parser (parser.py)
Абстрактный базовый класс для всех парсеров данных о вакансиях:
```python
@abstractmethod
def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]
```

### HH (hh.py)
Конкретная реализация для API HeadHunter:
- Корректная обработка API запросов к hh.ru
- Автоматическое преобразование ответов в структурированные данные
- Обработка ошибок соединения и API
- Получение детальной информации о вакансиях

### Vacancy (vacancy.py)
Модель данных вакансии с использованием `__slots__`:
- Валидация типов данных при создании объекта
- Методы сравнения по зарплате (`__lt__`, `__le__`, `__gt__`, `__ge__`)
- Сериализация в dict/JSON
- Статические методы для создания объектов из различных форматов данных

### FileHandler (file_handler.py)
Абстрактный класс для работы с хранилищем данных:
```python
@abstractmethod
def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None
@abstractmethod
def delete_vacancy(self, vacancy_id: str) -> None
@abstractmethod
def filter_vacancies(self, filter_words: List[str]) -> List[Dict[str, Any]]
@abstractmethod
def filter_vacancies_by_salary(self, salary_range: Tuple[int, int]) -> List[Dict[str, Any]]
@abstractmethod
def get_all_vacancies(self) -> List[Dict[str, Any]]
```

### JSONSaver (json_saver.py)
Конкретная реализация хранилища вакансий в формате JSON:
- Автоматическое создание файла и директорий
- Избежание дубликатов по ID вакансии
- CRUD операции (Create, Read, Update, Delete)
- Безопасная работа с файловой системой

## Тестирование

Проект включает 81 тест, покрывающий все основные компоненты системы.

### Запуск тестов через Poetry (рекомендуется)

```bash
# Все тесты с подробным выводом
poetry run pytest tests/ -v

# Быстрый прогон всех тестов
poetry run pytest tests/

# С покрытием кода
poetry run pytest tests/ --cov=src --cov-report=html

# Конкретный тест-файл
poetry run pytest tests/test_vacancy.py -v

# Конкретный тест-класс
poetry run pytest tests/test_vacancy.py::TestVacancy -v

# Конкретный тест-метод
poetry run pytest tests/test_vacancy.py::TestVacancy::test_vacancy_init_valid -v

# Тесты с кратким выводом ошибок
poetry run pytest tests/ -v --tb=short

# Показать статистику пройденных тестов
poetry run pytest tests/ --tb=no -q
```

### Альтернативно через venv

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Запуск тестов
pytest tests/ -v

# С покрытием кода
pytest tests/ --cov=src --cov-report=html
```

### Структура тестов

Тесты организованы по компонентам:
- `test_cli.py` (25 тестов) - тестирование консольного интерфейса
- `test_file_handler.py` (4 теста) - тесты абстрактного класса FileHandler
- `test_hh.py` (6 тестов) - тестирование HeadHunter API
- `test_json_saver.py` (12 тестов) - тесты JSON хранилища
- `test_parser.py` (5 тестов) - тесты абстрактного класса Parser  
- `test_utils.py` (17 тестов) - тесты утилит фильтрации и сортировки
- `test_vacancy.py` (12 тестов) - тесты модели вакансии

**Итого: 81 тест**

### Покрытие кода

Для просмотра HTML-отчёта о покрытии кода:
```bash
poetry run pytest tests/ --cov=src --cov-report=html
# Откройте файл htmlcov/index.html в браузере
```

## Пример использования

```python
from src.hh import HH
from src.json_saver import JSONSaver
from src.vacancy import Vacancy
from src.utils import filter_vacancies, sort_vacancies

# Создание API и хранилища
api = HH()
storage = JSONSaver("my_vacancies.json")

# Поиск вакансий
print("Подключение к HeadHunter API...")
api.connect()

print("Поиск вакансий...")
vacancies_data = api.load_vacancies("Python разработчик")

# Преобразование в объекты Vacancy
vacancies = Vacancy.cast_to_object_list(vacancies_data)

# Сохранение в файл
print(f"Сохранение {len(vacancies)} вакансий...")
for vacancy in vacancies:
    storage.add_vacancy(vacancy.to_dict())

# Фильтрация по зарплате
high_salary_vacancies = get_vacancies_by_salary(vacancies, (100000, 200000))

# Сортировка по убыванию зарплаты
sorted_vacancies = sort_vacancies(high_salary_vacancies, reverse=True)

# Топ-10 по зарплате
top_vacancies = get_top_vacancies(sorted_vacancies, 10)

# Вывод результатов
print_vacancies(top_vacancies)
```

### Консольный интерфейс

```python
from src.cli import user_interaction

# Запуск интерактивного режима
if __name__ == "__main__":
    user_interaction()
```

## Формат данных вакансии

```json
{
    "id": "125338404",
    "name": "Python разработчик",
    "alternate_url": "https://hh.ru/vacancy/125338404",
    "salary_from": 100000.0,
    "salary_to": 140000.0, 
    "salary_currency": "RUR",
    "area_name": "Москва",
    "requirement": "Опыт разработки на Python от 2 лет",
    "responsibility": "Разработка backend сервисов",
}
```

## Обработка ошибок

- Корректная обработка HTTP ошибок API
- Валидация входных данных
- Graceful degradation при отсутствии интернета
- Информативные сообщения об ошибках

## Особенности реализации

### Оптимизация памяти
- Класс `Vacancy` использует `__slots__` для экономии памяти
- Ленивая инициализация больших объектов

### Безопасность
- API ключи в переменных окружения
- Валидация всех пользовательских вводов
- Безопасная работа с файловой системой

### Производительность
- Кэширование результатов API запросов
- Пагинация для больших объемов данных  
- Оптимизированная сериализация JSON

## Расширяемость

Архитектура позволяет легко добавить:
- Новые источники вакансий (SuperJob API, Rabota.ru и др.)
- Другие форматы хранения (XML, CSV, БД)
- Дополнительные фильтры и сортировки
- GUI интерфейс

## Автор
Казанцев Андрей
Курсовая работа по дисциплине "Программирование на Python"  
Тема: "Поиск вакансий. API и библиотека requests"

## Лицензия


```
MIT License