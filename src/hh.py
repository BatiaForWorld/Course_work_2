from typing import Any, Dict, List

import requests

from .parser import Parser


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        """
        Инициализация класса для работы с API HeadHunter
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        }
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        super().__init__(file_worker)

    def _connect(self) -> None:
        """
        Приватный метод подключения к API HeadHunter (проверка доступности)
        """
        try:
            response = requests.get(self.__url, headers=self.__headers, params={"text": "test", "per_page": 1})
            if response.status_code != 200:
                raise ConnectionError(f"Ошибка подключения к API hh.ru: {response.status_code}")
        except Exception as e:
            raise ConnectionError(f"Ошибка подключения к API hh.ru: {str(e)}")

    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Метод загрузки вакансий с API HeadHunter
        """
        self._connect()

        self.__params["text"] = keyword
        self.__params["page"] = 0
        self.__vacancies = []

        while self.__params.get("page") < 20:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code != 200:
                    break

                data = response.json()
                vacancies = data.get("items", [])

                if not vacancies:
                    break

                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1

            except requests.RequestException:
                break

        return self.__vacancies
