import re

from binance.spot import Spot

from dotenv import dotenv_values

from Telegram import telegramBot

config = dotenv_values()

client = Spot(key=config["key"], secret=config["secret"])

tickerPriceChange = client.ticker_24hr()

def check24hDips():
    pairs = []
    for pair in tickerPriceChange:    
        if (re.search('(USDT)$',pair["symbol"]) is not None)  and (float(pair["priceChangePercent"]) < -10.000) and ('DOWN' not in pair["symbol"]) and ('UP' not in pair["symbol"]):                        
        # if (re.search('(USDT)$',pair["symbol"]) is not None)  and (float(pair["priceChangePercent"]) < -10.000):            
            # print(pair)
            # print(f"-----------------")
            # telegramBot.announceDip(pair)
            pairs.append(pair)
            return pairs