from trader import Trader
from random import randint

from order import Order

id = 0

def next_id() -> int:
    global id 
    id += 1
    return id


def random_100(trader: Trader):
    if randint(0, 100) % 2 == 0:
        # sell
        return [Order("sell", 100 + randint(-5, 5), randint(0, trader.jcoin), trader, next_id())]
    else:
        # buy
        return [Order("buy", 100 + randint(-5, 5), randint(0, trader.usd), trader, next_id())]


strategyes = [random_100]