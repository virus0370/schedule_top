from pprint import pprint

import requests
import json

url = "https://msapi.top-academy.ru/api/v2/auth/login"

payload = json.dumps({
  "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
  "id_city": None,
  "password": "AcTop28099",
  "username": "gariz_oe01"
})
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru_RU, ru',
  'authorization': 'Bearer null',
  'content-type': 'application/json',
  'origin': 'https://journal.top-academy.ru',
  'priority': 'u=1, i',
  'referer': 'https://journal.top-academy.ru/',
  'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
  'sec-ch-ua-platform-version': '"6.0"',
  'Referer': 'https://journal.top-academy.ru/ru/main/dashboard/page/index',
  'sec-ch-ua-model': '"Nexus 5"',
  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
  'cookie': 'advcake_track_id=5ada5932-4136-f331-4db8-447cb6cd0db9; advcake_session_id=5c08218c-cf47-8c31-bfc8-031222fddf2f; roistat_visit=12991841; roistat_first_visit=12991841; roistat_visit_cookie_expire=1209600; roistat_marker=seo_yandex_search; roistat_marker_old=seo_yandex_search; cf_clearance=CeEukqrBTqbnySLAldR.UWUzqx8J3wE4ZSn97We5DLw-1717622279-1.0.1.1-YxUo1RB4Xx5UwfjdrD2fJA_aXZbojb1wVlxExcXWjKumx7at8oWBvUbOCd8r02cZZ3kYeDX.03FGIaVPmcT4lw'
}

response = requests.request("POST", url, headers=headers, data=payload)

response_data = response.json()  # Преобразование ответа в словарь (если он JSON)
access_token = response_data.get('access_token', '')
refresh_token = response_data.get('refresh_token', '')
print("Access token:", access_token)
print("Refresh token:", refresh_token)


url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter=2024-06-06"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru_RU, ru',
  'authorization': f'Bearer {refresh_token}',
  'origin': 'https://journal.top-academy.ru',
  'priority': 'u=1, i',
  'referer': 'https://journal.top-academy.ru/',
  'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
  'Cookie': '_csrf=8sBn0AJCDdUVlnW-XICKsAEhtSQnMK2U'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


# -*- coding: utf-8 -*-

# Импортируем библиотеку для работы с датами
from datetime import datetime


# Преобразуем строку JSON в список словарей
schedule = eval(response.text)

# Генерируем красивое сообщение для aiogram
message = "Расписание на июнь:\n"
for lesson in schedule:
    # Преобразуем строку с датой в объект datetime
    lesson_date = datetime.strptime(lesson['date'], '%Y-%m-%d')
    # Форматируем дату в удобный вид (день.месяц)
    lesson_date_formatted = lesson_date.strftime('%d.%m')
    # Формируем текст для каждого занятия
    lesson_text = f"{lesson_date_formatted}, {lesson['started_at']}-{lesson['finished_at']}:\n"\
                  f"{lesson['subject_name']}\n"\
                  f"Преподаватель: {lesson['teacher_name']}\n"\
                  f"Аудитория: {lesson['room_name']}\n\n"
    # Добавляем текст занятия к общему сообщению
    message += lesson_text

# Выводим сообщение
print(message)


import requests

url = "https://msapi.top-academy.ru/api/v2/settings/user-info"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru_RU, ru',
  'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbXNhcGkuaXRzdGVwLm9yZyIsImlhdCI6MTcxNzYyNTU1OSwiYXVkIjoxLCJleHAiOjE3MTc2NTQzNTksImFwaUFwcGxpY2F0aW9uSWQiOjEsImFwaVVzZXJUeXBlSWQiOjEsInVzZXJJZCI6NTAsImlkQ2l0eSI6Mzk5fQ.7PHcJR_xot-jTPYBE2id6eH0dySnZXXjPfBNrn8-I8o',
  'origin': 'https://journal.top-academy.ru',
  'priority': 'u=1, i',
  'referer': 'https://journal.top-academy.ru/',
  'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
  'Cookie': '_csrf=8sBn0AJCDdUVlnW-XICKsAEhtSQnMK2U'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

