## A simlpe currency crawler

Basically, this crawler implements the crawling of specific currency history data on https://coinmarketcap.com, and its output data format can be found on the following page：

<img src="https://i.loli.net/2021/06/03/3MeqaQWLrImBpcK.png" alt="image-20210603191606754" style="zoom:50%;" />

The output data is in .csv format:

<img src="https://i.loli.net/2021/06/03/OrxIHqVpgmoKu5k.png" alt="image-20210603192058468" style="zoom:50%;" />



### Basic functionalities

- Get data on the current top 1 to 5000 currencies
- Get data for the currency (currencies) of the given specified name(s)



### How to use

For convenience, I have written a simple command line client. 

To get the usage of this client, simply input  `python client.py -h`

![image-20210604151244954](https://i.loli.net/2021/06/04/uhAcSEx8Lf6d2ps.png)

Examples:

1. To get the data of top 100 currencies of year 2020：

    ```
    python client.py 2020-01-01 2021-01-01 -l 100
    ```

    You can use `-l` or `--limit` to set the number of currencies you want to crawl, and use `-i` or `--index` to specify the start index:

    ```
    python client.py 2020-01-01 2021-01-01 -l 100 -i 500
    ```

    The code above crawl the data of currencies ranked from 500 to 600.

2. To obtain currency data by name

    - To get the data of Bitcoin of year 2019:

        ```
        python client.py 2019-01-01 2020-01-01  -n "Bitcoin"
        ```

    - To get the data of Bitcoin & Cardano, first create a file `test.txt`:

        ```
        Bitcoin
        Cardano
        ```

        Then use `-f` or `--file`

        ```
        python client.py 2019-01-01 2020-01-01  -f ./test.txt
        ```

3. A currency to ID mapping is stored locally and you can use your own API key to update the local mapping. By default the first 5000 entries are updated, you can change this setting in the source code. Use `-a` or `--api` to do this:

    ```
    python client.py -a <your_api_key>
    ```

### Cautions

- ⚠️ Python ***version >= 3.7*** required
- ⭕️ If any library missing, use `pip`/`pip3` to install them.
- 😭 As this crawler has not been rigorously tested, there may be unexpected bugs. You can ***issue*** or ***pull requests*** if you have any advice to improve this simple project.

