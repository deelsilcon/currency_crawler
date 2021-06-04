import asyncio
import time
from collections import OrderedDict
import aiohttp
import pandas as pd


class SimpleCrawler:
    local_map = OrderedDict()

    def __init__(self):
        self.read_id_map_from("./map_data.txt")

    @staticmethod
    def process_strings(s: str):
        s = s.replace("\n", "")
        s = s.replace("/", "")
        s.strip()
        return s

    async def get_page(self, cid, currency_name, time_start, time_end):
        """
        Get a specified page's data

        :param cid: currency id
        :param currency_name: currency_name
        :param time_start: the start time (seconds from unix epoch)
        :param time_end: the end time (seconds from unix epoch)
        :return: None
        """
        with aiohttp.TCPConnector(ssl=False) as conn:
            currency_name = currency_name.replace("\n", "")

            url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={cid}&convertId=2787&timeStart={time_start}" \
                  f"&timeEnd={time_end}"
            print(url)
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            headers = {"User-Agent": user_agent}
            async with aiohttp.request('GET', url, headers=headers, connector=conn) as r:
                if r.status != 200:
                    print(f"Url: {url}")
                    print(f"Error response with response code {r.status}")
                    return -1
                content = await r.json(encoding='utf-8')
                data = content['data']['quotes']
                self.process_data(currency_name, data)

    def process_data(self, currency_name, data):
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
        currency_name = SimpleCrawler.process_strings(currency_name)
        df.to_csv(f'./data/{currency_name}.csv', encoding="utf-8", index=False)
        print(f"Successfully export data to {currency_name}.csv!")

    def look_for_id(self, currency_name):
        """
        A helper method which returns the id of given currency.

        :param currency_name: the name of the currency
        :return: 0 for success and -1 for failure
        """
        currency_name = SimpleCrawler.process_strings(currency_name)
        return self.local_map.get(currency_name, -1)

    def crawl_single_currency(self, currency_name, start_time, end_time):
        """
        Crawl data for one currency.

        :param currency_name: the name of the currency
        :param start_time: the start time (seconds from unix epoch)
        :param end_time: the end time (seconds from unix epoch)
        :return: 0 for success and -1 for failure
        """
        cid = self.look_for_id(currency_name)
        if cid != -1:
            loop = asyncio.get_event_loop()
            tasks = asyncio.gather(
                *[self.get_page(cid, currency_name, start_time, end_time)])
            loop.run_until_complete(tasks)
            return 0
        else:
            return -1

    def crawl_list_currency(self, file_name, start_time, end_time):
        """
        Crawl data for some currencies.

        :param file_name: path of the file
        :param start_time: the start time (seconds from unix epoch)
        :param end_time: the end time (seconds from unix epoch)
        :return: None
        """
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                name = file.readline()
                groups = []
                while name is not None and len(name) != 0:
                    name = SimpleCrawler.process_strings(name)
                    groups.append((name, self.local_map.get(name)))
                    name = file.readline()
                loop = asyncio.get_event_loop()
                tasks = asyncio.gather(
                    *[self.get_page(groups[i][1], groups[i][0], start_time, end_time) for i in range(len(groups))])
                loop.run_until_complete(tasks)
            print("Successfully crawl data of given currencies.")
        except Exception as e:
            print(e)
            print("Something wrong! Check the file and code!")

    def read_id_map_from(self, file_path):
        """
        read IDs from local map

        :param file_path:
        :return: None
        """
        with open(file_path, "r", encoding="utf=8") as file:
            line = file.readline()
            while line is not None and len(line) != 0:
                data = line.split(":")
                name = SimpleCrawler.process_strings(data[0])
                currency_id = SimpleCrawler.process_strings(data[-1])
                line = file.readline()
                self.local_map[name] = int(currency_id)

    def run_multi_query(self, index, limit, begin, end):
        """
        Run many queries asynchronously to get multiple currencies' data

        :param index: the start index
        :param limit: the number of currency we want to crawl
        :param begin: the start time (seconds from unix epoch)
        :param end: the end time (seconds from unix epoch)
        :return: None
        """
        start = time.time()
        loop = asyncio.get_event_loop()
        currencies_names = [ele for ele in self.local_map.keys()]
        ids = [self.local_map.get(i) for i in currencies_names]
        tasks = asyncio.gather(
            *[self.get_page(ids[i], currencies_names[i], begin, end) for i in range(index, index + limit)])
        loop.run_until_complete(tasks)
        end = time.time()
        print(f"it takes {end - start} seconds to finish!")


if __name__ == '__main__':
    crawler = SimpleCrawler()
    print(crawler.look_for_id("Bitcoin\n"))
    print(crawler.look_for_id("Cardano\n"))
