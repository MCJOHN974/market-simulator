import pandas as pd
import mplfinance as mpf
import datetime
from exchange import Exchange
from order import Order
from trader import Trader
import strategyes
from random import randint


AMOUNT_OF_TRADING_DAYS = 1000
AMOUNT_OF_TRADERS = 300
TRADES_IN_DAY = 50

def plot_candlestick(ohlc_data):
    # Create a market colors object
    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)

    # Create a style based on the market colors
    s = mpf.make_mpf_style(marketcolors=mc)

    # Create the plot with the style
    mpf.plot(ohlc_data, type='candle', style=s)


def process_data(data):
    ohlc_data = []
    prices_only = list(map(lambda trade: (trade["buy_price"] + trade["sell_price"]) / 2, data))
    days = [prices_only[i:i+TRADES_IN_DAY] for i in range(0,len(prices_only),TRADES_IN_DAY)]
    for day in days:
        if not day:  # skip empty days
            continue
        open_price = day[0]
        high_price = max(day)
        low_price = min(day)
        close_price = day[-1]
        ohlc_data.append((open_price, high_price, low_price, close_price))
    date_index = pd.date_range(start=datetime.datetime.today(), periods=len(ohlc_data))
    print(date_index)
    return pd.DataFrame(ohlc_data, columns=["Open", "High", "Low", "Close"], index=date_index)

import strategyes


def get_strategy():
    x = randint(1, 100)


    
    if x < 10:
        return strategyes.buyer
    if x < 20:
        return strategyes.seller
    if x < 30:
        return strategyes.analyst_volatile
    if x < 40:
        return strategyes.analyst
    if x < 42:
        return strategyes.pumper
    if x < 45:
        return strategyes.dumper
    if x < 50:
        return strategyes.pumperdumper
    if x < 70:
        return strategyes.hamster
    return strategyes.hamster_volatile



def generate_traders(exchange: Exchange):
    res = []
    for _ in range(AMOUNT_OF_TRADERS):
        res.append(Trader(exchange, get_strategy()))
        if res[-1] == strategyes.pumper:
            res[-1].deposit_usd(randint(1000000, 10000000000000000))
        if res[-1] == strategyes.dumper:
            res[-1].deposit_jcoin(randint(100000, 1000000000000000))
        if res[-1] == strategyes.pumperdumper:
            res[-1].deposit_usd(randint(1000000, 10000000000000000))
            res[-1].deposit_jcoin(randint(100000, 1000000000000))
        res[-1].deposit_usd(randint(100000, 10000000000))
        res[-1].deposit_jcoin(randint(10000, 1000000000))
    return res


def main():
    # Create an exchange
    exchange = Exchange()
    traders = generate_traders(exchange)

    for _ in range(AMOUNT_OF_TRADING_DAYS):
        for trader in traders:
            trader.generate_orders()
        exchange.match_orders()



    with open("trades.txt", "w") as tradelog:
        tradelog.writelines(str(exchange.trades()))


    data = exchange.trades()
    # Process data
    ohlc_data = process_data(data)
    # Plot the chart
    plot_candlestick(ohlc_data)



if __name__ == "__main__":
    main()
