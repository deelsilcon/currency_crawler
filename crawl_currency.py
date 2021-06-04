import grequests
import requests
import json
import pandas as pd
from get_id_map import get_id_map

currency_names = []
ids = []


def scrapy_data(cid, time_start, time_end, currency_name):
    """
    Scrapy data from https://coinmarketcap.com and store in corresponding
    .csv file.\n
    The stored data format is:
    Date,OpeningPrice,HighestPrice,LowestPrice,ClosingPrice,Volume,MarketCap
    For the `cid` field, find it in the corresponding page in the web or use
    the developer's API .
    :param cid: id of corresponding currency
    :param time_start: the start time (seconds from unix epoch)
    :param time_end: the end time (seconds from unix epoch)
    :param currency_name: the name of the currency
    :return: 0 for success and -1 for failure
    """
    currency_name = currency_name.replace("\n", "")
    url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={cid}&convertId=2787&timeStart={time_start}" \
          f"&timeEnd={time_end}"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
    headers = {"User-Agent": user_agent}
    with requests.get(url=url, headers=headers) as response:
        if response.status_code == 200:
            content = response.content.decode("gbk")
            data = json.loads(content)['data']['quotes']
            process_data(currency_name, data)
            return 0
        else:
            print(f"Error response with response code {response.status_code}")
            return -1


def process_data(currency_name, data):
    """
    Process the data crawled from web page and export as .csv file.

    :param currency_name: the name of the currency
    :param data: crawled data
    :return: None
    """
    df = pd.DataFrame()
    for element in data:
        quote = element['quote']
        record = {"Date": element['timeOpen'][:10], "OpeningPrice": quote['open'], "HighestPrice": quote['high'],
                  "LowestPrice": quote['low'], "ClosingPrice": quote['close'],
                  "Volume": quote['volume'],
                  "MarketCap": quote['marketCap']}
        df = df.append([record])
    df.to_csv(f'./data/{currency_name}.csv', encoding="utf-8", index=False)
    print(f"Successfully export data to {currency_name}.csv!")


def look_for_id(currency_name):
    """
    A helper method which returns the id of given currency.

    :param currency_name: the name of the currency
    :return: 0 for success and -1 for failure
    """
    currency_name = currency_name.replace("\n", "")
    with open("./map_data.txt", "r", encoding="utf=8") as file:
        line = file.readline()
        while line is not None and len(line) != 0:
            data = line.split(":")
            name = data[0].replace("\n", "")
            if name == currency_name:
                return int(data[-1].replace("\n", ""))
            line = file.readline()
    return -1


def crawl_single_currency(currency_name, start_time, end_time, api_key):
    """
    Crawl data for one currency.

    :param currency_name: the name of the currency
    :param start_time: the start time (seconds from unix epoch)
    :param end_time: the end time (seconds from unix epoch)
    :param api_key: your private api key, for more info: https://pro.coinmarketcap.com/account
    :return: 0 for success and -1 for failure
    """
    cid = look_for_id(currency_name)
    if cid != -1:
        if scrapy_data(cid, start_time, end_time, currency_name) == -1:
            return -1
        else:
            return 0
    else:
        if get_id_map(api_key) == -1:
            print("Wrong API key! Check your API key and try again!")
            return -1
        cid = look_for_id(currency_name)
        if cid != -1:
            if scrapy_data(cid, start_time, end_time, currency_name) == -1:
                return -1
            else:
                return 0
        else:
            return -1


def crawl_list_currency(file_name, start_time, end_time, api_key):
    """
    Crawl data for some currencies.

    :param file_name: path of the file
    :param start_time: the start time (seconds from unix epoch)
    :param end_time: the end time (seconds from unix epoch)
    :param api_key: your private api key, for more info: https://pro.coinmarketcap.com/account
    :return: 0 for success and -1 for failure
    """
    with open(file_name, "r", encoding="utf-8") as file:
        name = file.readline()
        while name is not None and len(name) != 0:
            if crawl_single_currency(name, start_time, end_time, api_key) == -1:
                return -1
            name = file.readline()
    return 0


def read_id_map_from(file_name, currency_names, ids):
    """
    read IDs from local map

    :param file_name: the path of the map file (default ./map_data.txt)
    :param currency_names: output list that contains currencies' names
    :param ids: output list contains currencies' IDs
    :return: None
    """
    with open(file_name, "r", encoding="utf=8") as file:
        line = file.readline()
        cnt = 0
        while line is not None and len(line) != 0:
            cnt += 1
            data = line.split(":")
            name = data[0]
            currency_id = data[-1]
            currency_names.append(name.strip())
            ids.append(int(currency_id))
            line = file.readline()
        print(f"Successfully read {cnt} record(s) from map")


def run(tp):
    """
    Run!!!

    :param limit: the number of currency we want to crawl
    :param start_date: the start time (seconds from unix epoch)
    :param end_date: the end time (seconds from unix epoch)
    :return: None
    """
    lb, ub, start_date, end_date, t = tp
    cnt = 0
    currency_names.clear()
    ids.clear()
    read_id_map_from("./map_data.txt", currency_names, ids)
    ub = min(ub, t)
    for i in range(lb, ub):
        scrapy_data(ids[i], start_date, end_date, currency_names[i])
        cnt += 1
    print(f"Successfully crawl {cnt} record(s)")
