import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests


def get_map_scale(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    envelope = toponym['boundedBy']['Envelope']
    lb = envelope['lowerCorner'].split()
    lb_long, lb_lat = float(lb[0]), float(lb[1])
    rt = envelope['upperCorner'].split()
    rt_long, rt_lat = float(rt[0]), float(rt[1])
    delta_lat = abs(rt_lat - lb_lat)
    delta_long = abs(rt_long - lb_long)
    return (delta_lat, delta_long)
