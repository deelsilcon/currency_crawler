## A simlpe currency crawler

Basically, this crawler implements the crawling of specific currency history data on https://coinmarketcap.com, and its output data format can be found on the following page：

<img src="https://i.loli.net/2021/06/03/3MeqaQWLrImBpcK.png" alt="image-20210603191606754" style="zoom:50%;" />

The output data is in .csv format:

<img src="https://i.loli.net/2021/06/03/OrxIHqVpgmoKu5k.png" alt="image-20210603192058468" style="zoom:50%;" />



### Basic functionalities

- Get data on the current top 1 to 5000 currencies
- Get data for the currency (currencies) of the given specified name(s)



### How to use

First, get your own API key from [CoinMarketCap](https://coinmarketcap.com/api/). Simply register and log in, it's easy. ![image-20210603195623080](https://i.loli.net/2021/06/03/gDOIuvswKhFVAaS.png)

For convenience, I have written a simple command line client. To get the usage, input  `python client.py -h`

![image-20210603194225048](https://i.loli.net/2021/06/03/OV89bzHBYTLXKx5.png)

Examples:

1. To get the data of top 100 currencies of year 2020：

    ```
    python client.py 2020-01-01 2021-01-01 -l 100
    ```

     Note that if API key is not given, this crawler will use local map (i.e. ./map_data.txt) for crawling.

2. To obtain currency data by name, you need to provide the API key. Use `-a` or `--api` to do this.

    - To get the data of Bitcoin of year 2019:

        ```
        python client.py 2019-01-01 2020-01-01 -a <your_api_key> -n "Bitcoin"
        ```

    - To get the data of Bitcoin & Cardano, first create a file `test.txt`:

        ```
        Bitcoin
        Cardano
        ```

        Then use `-f` or `--file`

        ```
        python client.py 2019-01-01 2020-01-01 -a <your_api_key> -f ./test.txt
        ```

    - You can use `-l` or `--limit` to set the number of currencies you want to crawl, and use `-i` or `--index` to specify the start index
    
        ```
        python client.py 2020-01-01 2021-01-01 -l 100 -i 500
        ```
    
        The code above crawl the data of currencies ranked from 500 to 600.

### Cautions

- ⚠️ Python version >= 3.7 required
- 🌝 For query by name(s), i simply write a linear scan to search for the given name's corresponding id, so it may be a little bit slow now. By the way, every map update takes one credit, for more information, check out:[CoinMarketCap API Documentation](https://coinmarketcap.com/api/documentation/v1/)
- ⭕️ If any library missing, use `pip`/`pip3` to install them.
- 😭 As this crawler has not been rigorously tested, there may be unexpected bugs:
    - 😅 I am sorry, but because I accidentally used a synchronous IO model, it is best to keep the maximum number of records fetched at one time under 300. Requests with a number above 300 may cause IO blocking. This will be fixed sooner.

