# telegram
scripts and bots for telegram

## install [python-telegram-bot](https://python-telegram-bot.org/) package with [PIP](https://pypi.org/project/python-telegram-bot/)
``` pip install python-telegram-bot```

## Function
- Query all the cryptocurrency's price data in realtime
- Query historical bitcoin price (require price data yielded from [this source](http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz))
- Basic user input logging

### Note
run ```python updatePriceData.py``` first. 

updatePriceData.py fetches coinbase BTCUSD trade history and outputs a date-price json file (one point per minute) required for this bot.