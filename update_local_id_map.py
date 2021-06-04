import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def update_local_id_map( api_key):
    """
    Get IDs map
    :param api_key: your private api key
    :return: 0 for success and -1 for failure
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': 1,
        'limit': 5000,
        'sort': 'cmc_rank'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f"{api_key}",
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
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
