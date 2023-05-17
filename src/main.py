import pandas as pd
import mplfinance as mpf
import datetime
from exchange import Exchange
from order import Order
from trader import Trader
import strategyes
from random import randint


AMOUNT_OF_TRADING_DAYS = 100
AMOUNT_OF_TRADERS = 1000
TRADES_IN_DAY = 3

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

    return pd.DataFrame(ohlc_data, columns=["Open", "High", "Low", "Close"], index=date_index)


def generate_traders(exchange: Exchange):
    res = []
    for _ in range(AMOUNT_OF_TRADERS):
        res.append(Trader(exchange, strategyes.strategyes[randint(0, len(strategyes.strategyes) - 1)]))
        res[-1].deposit_usd(randint(100, 100000))
        res[-1].deposit_jcoin(randint(1, 1000))
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
