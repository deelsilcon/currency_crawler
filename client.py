import argparse
import sys
from datetime import datetime

from crawl_currency import CurrencyCrawl
from get_id_map import get_id_map


def process_date(date):
    t = datetime.strptime(date, "%Y-%m-%d")
    return int(t.timestamp())


def check():
    if sys.version_info.major * 10 + sys.version_info.minor < 37:
        print("Minimum python interpreter version required: 3.7! Sorry!")
        sys.exit(1)


def main():
    check()
    crawl = CurrencyCrawl()
    string_desc = "A simple crawler for historical data of cryptocurrencies. Be careful to input date with " \
                  "format Y-M-D. "
    parser = argparse.ArgumentParser(description=string_desc)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("start", help="The start date(format Y-M-D) of the data")
    parser.add_argument("end", help="The end date(format Y-M-D) of the data")
    parser.add_argument("-a", '--api',
                        help="Private API key used for updating the IDs map. If not specified, use local map instead")
    parser.add_argument("-l", '--limit', help="The number of currencies to crawl (1-5000). If not specified, use 50 "
                                              "as default", default=50, type=int)
    group.add_argument("-n", '--name',
                       help="Used for crawl single currency. Notice that by setting this parameter, limit will be "
                            "ignored.")
    group.add_argument("-f", '--file',
                       help="Crawl currencies with names specified in a file. Only one name is allowed per line")
    parser.add_argument('-v', '-version', action='version',
                        version='simple_crawler version : v 0.01', help='Show the version')
    args = parser.parse_args()
    start = args.start
    end = args.end
    api_key = args.api
    name = args.name
    limit = args.limit
    file = args.file
    start_date = process_date(start)
    end_date = process_date(end)
    if file is not None:
        if crawl.crawl_list_currency(file, start_date, end_date, api_key) == -1:
            print("Something wrong! Plz check the names in the file.")
            sys.exit(1)
        else:
            print("Crawl currencies finished!")
            sys.exit(0)
    if name is not None:
        print(name)
        if api_key is None:
            print("Please offer your API key!")
            sys.exit(1)
        else:
            if crawl.crawl_single_currency(name, start_date, end_date, api_key) == -1:
                print(f"Sorry, can't find coin {name}")
                sys.exit(1)
            else:
                print(f"Crawl {name} finished!")
                sys.exit(0)
    if api_key is not None:
        if get_id_map(limit, api_key) == -1:
            print("Wrong API key! Check your API key and try again!")
            sys.exit(1)
    crawl.run(limit, start_date, end_date)


if __name__ == '__main__':
    main()