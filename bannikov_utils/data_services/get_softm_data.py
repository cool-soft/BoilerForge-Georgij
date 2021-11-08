from time import sleep

import requests

SERVER_URL = "https://chern.agt.town/json/"


def get_data_from_server(url: str = SERVER_URL, params: dict = {}, echo: bool = True):
    connection = False
    lost = False
    try_count = 1
    while not connection:
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            connection = True
        except:
            if not lost:
                print(f"\n Попытка соединения с {url}: {try_count}", end=" ")
                lost = True
            else:
                print(try_count, end=" ")
            connection = False
        sleep(10)
        try_count += 1

    if lost:
        print("")

    if resp.status_code != 200:
        print("Ошибка отправки запроса: \n\t", resp.url)
        return []
    if echo:
        print("<get_data_from_server>: Запрос успешно отправлен и получен ответ.")
    # print(resp.json()["data"])
    return resp.json()["data"]
