import json

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_id_map(limit, api_key):
    """
    Get IDs map
    :param limit: the number of currency id we want to store locally
    :param api_key: your private api key
    :return: 0 for success and -1 for failure
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': '1',
        'limit': f'{limit}',
        'sort': 'cmc_rank'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f"{api_key}",
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code != 200:
            return -1
        data = json.loads(response.text)
        dic = data['data']
        with open("map_data.txt", "w+", encoding="utf-8") as file:
            for d in dic:
                file.write(f"{d['name']}:{d['id']}\n")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return -1
    return 0