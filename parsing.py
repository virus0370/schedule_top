import requests
import json


def get_token(username, password):
    url = "https://msapi.top-academy.ru/api/v2/auth/login"
    payload = {
        "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "id_city": None,
        "password": password,
        "username": username
    }
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

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get('access_token', '')
        refresh_token = response_data.get('refresh_token', '')
        return access_token, refresh_token
    else:
        return None


def get_user_info(token):
    url = "https://msapi.top-academy.ru/api/v2/settings/user-info"
    payload = {}

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': f'Bearer {token}',
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

    if response.status_code == 200:
        response_data = response.json()
        return response_data


def get_schedule(token, date_filter):
    url = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={date_filter}"
    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': f'Bearer {token}',
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

    if response.status_code == 200:
        response_data = response.json()
        return response_data
