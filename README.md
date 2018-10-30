# telegram
scripts and bots for telegram

## install [python-telegram-bot](https://python-telegram-bot.org/) package with [PIP](https://pypi.org/project/python-telegram-bot/)
``` pip install python-telegram-bot```

## Function
- Query all the cryptocurrency's price data in realtime. Source: [https://coinmarketcap.com/](https://coinmarketcap.com/)
- Query historical bitcoin price. Source: [http://bitcoincharts.com/](http://bitcoincharts.com/)
- Basic user input logging
- Basic deterministic tree-based chat.

### Note
run ```python updatePriceData.py``` first. 

updatePriceData.py fetches coinbase BTCUSD trade history and outputs a date-price json file (one point per minute) required for this bot.
