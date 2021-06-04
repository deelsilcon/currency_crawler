import argparse
import sys
from datetime import datetime
from crawl_currency import *
from update_local_id_map import *


def process_date(date):
    t = datetime.strptime(date, "%Y-%m-%d")
    return int(t.timestamp())


def check():
    if sys.version_info.major * 10 + sys.version_info.minor < 37:
        print("Minimum python interpreter version required: 3.7! Sorry!")
        sys.exit(1)


def main():
    check()
    crawler = SimpleCrawler()
    string_desc = "A simple crawler for historical data of cryptocurrencies. Be careful to input date with " \
                  "format Y-M-D. "
    parser = argparse.ArgumentParser(description=string_desc)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("start", help="The start date(format Y-M-D) of the data")
    parser.add_argument("end", help="The end date(format Y-M-D) of the data")
    parser.add_argument("-a", '--api',
                        help="Private API key used for updating the local IDs map")
    parser.add_argument("-l", '--limit', help="The number of currencies to crawl (1-5000). If not specified, use 50 "
                                              "as default", default=50, type=int)
    group.add_argument("-n", '--name',
                       help="Used to crawl single currency' data. Notice that by setting this parameter, limit will be "
                            "ignored.")
    group.add_argument("-i", '--index', help="The start index of the data we want to process.", default=0, type=int)
    group.add_argument("-f", '--file',
                       help="Crawl currencies with names specified in a file. Only one name is allowed per line")
    parser.add_argument('-v', '-version', action='version',
                        version='simple_crawler version : v 1.01', help='Show the version')
    args = parser.parse_args()
    start = args.start
    end = args.end
    api_key = args.api
    name = args.name
    limit = args.limit
    file = args.file
    index = args.index
    start_date = process_date(start)
    end_date = process_date(end)
    if file is not None:
        crawler.crawl_list_currency(file, start_date, end_date)
        sys.exit(0)

    if name is not None:
        if crawler.crawl_single_currency(name, start_date, end_date) == -1:
            print(f"Sorry, can't find coin {name}")
            sys.exit(1)
        else:
            print(f"Crawl {name} finished!")
            sys.exit(0)

    if api_key is not None:
        if update_local_id_map(api_key) == -1:
            print("Wrong API key! Check your API key and try again!")
            sys.exit(1)
        else:
            print("Successfully update local ID map")

    while limit > 400:
        crawler.run_multi_query(index + limit-400, index + limit, start_date, end_date)
        limit -= 400
        time.sleep(30)
        print("Waiting for next execution!")
    crawler.run_multi_query(index, index + limit, start_date, end_date)


if __name__ == '__main__':
    main()
