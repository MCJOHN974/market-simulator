from trader import Trader
from random import randint

from order import Order

PUMP_PROB = 20
DUMP_PROB = 10
BUY_PROB = 10
SELL_PROB = 10
ANALYST = 1.3

PUMP_DUMP_SPREAD = 7
HAMSTER_SPREAD = 1

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
    

def hamster_volatile(trader: Trader):
    exchange = trader.exchange
    if randint(0, 100) % 2 == 0:
        # sell
        lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100

        market_price = int((exchange.sell_orders[0].price + exchange.buy_orders[-1].price) / 2) if exchange.sell_orders != [] and exchange.buy_orders != [] else 100

        return [Order("sell", randint(lb, lb + HAMSTER_SPREAD), randint(0, int(trader.jcoin * (market_price) / 3)), trader, next_id())]
    else:
        # buy
        ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
        return [Order("buy", randint(ub - HAMSTER_SPREAD, ub), randint(0, int(trader.usd / 3)), trader, next_id())]
    

def hamster(trader: Trader):
    exchange = trader.exchange
    if randint(0, 100) % 2 == 0:
        # sell
        lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100
        market_price = int((exchange.sell_orders[0].price + exchange.buy_orders[-1].price) / 2) if exchange.sell_orders != [] and exchange.buy_orders != [] else 100
        return [Order("sell", lb, randint(0, int(trader.jcoin * market_price / 3)), trader, next_id())]
    else:
        # buy
        ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
        return [Order("buy", ub, randint(0, int(trader.usd / 3)), trader, next_id())]
    


def pumper(trader: Trader):
    if randint(0, PUMP_PROB) != 5:
        return []

    exchange = trader.exchange
    ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
    return [Order("buy", ub + PUMP_DUMP_SPREAD, trader.usd, trader, next_id())]
    

def dumper(trader: Trader):
    if randint(0, DUMP_PROB) != 5:
        return []

    exchange = trader.exchange
    lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100
     
    return [Order("sell", lb - PUMP_DUMP_SPREAD, trader.jcoin, trader, next_id())]


def buyer(trader: Trader):
    exchange = trader.exchange
    if randint(1, BUY_PROB) == 2:
        ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
        return [Order("buy", ub, randint(0, max(trader.usd, 50000000)), trader, next_id())]
    return []
    
def seller(trader: Trader):
    exchange = trader.exchange
    if randint(1, SELL_PROB) == 2:
        lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100
        return [Order("sell", lb, randint(0, max(trader.jcoin, 500000)), trader, next_id())]
    return []


def pumperdumper(trader: Trader):
    if randint(1, 100) % 2 == 0:
        return pumper(trader)
    return dumper(trader)

def analyst_volatile(trader: Trader):
    exchange = trader.exchange

    buy_volume = sum(map(lambda order: order.amount, exchange.buy_orders))
    sell_volume = sum(map(lambda order: order.amount, exchange.sell_orders))

    if buy_volume > ANALYST * sell_volume:
        ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
        return [Order("buy", randint(ub - HAMSTER_SPREAD, ub), randint(0, int(trader.usd / 3)), trader, next_id())]
    if sell_volume > ANALYST * buy_volume:
        lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100
        market_price = int((exchange.sell_orders[0].price + exchange.buy_orders[-1].price) / 2) if exchange.sell_orders != [] and exchange.buy_orders != [] else 100

        return [Order("sell", randint(lb, lb + HAMSTER_SPREAD), randint(0, int(trader.jcoin * market_price / 3)), trader, next_id())]
    return []


def analyst(trader: Trader):
    exchange = trader.exchange

    buy_volume = sum(map(lambda order: order.amount, exchange.buy_orders))
    sell_volume = sum(map(lambda order: order.amount, exchange.sell_orders))

    if buy_volume > ANALYST * sell_volume:
        ub = min(exchange.sell_orders).price if len(exchange.sell_orders) > 0 else 95
        return [Order("buy", ub, randint(0, int(trader.usd / 3)), trader, next_id())]
    if sell_volume > ANALYST * buy_volume:
        lb = max(exchange.buy_orders).price if len(exchange.buy_orders) > 0 else 100
        market_price = int((exchange.sell_orders[0].price + exchange.buy_orders[-1].price) / 2) if exchange.sell_orders != [] and exchange.buy_orders != [] else 100

        return [Order("sell", lb, randint(0, int(trader.jcoin * market_price / 3)), trader, next_id())]
    return []



# def sofisticated_analyst(trader: Trader):
#     exchange = trader.exchange

#     if exchange.buy_orders == [] or exchange.sell_orders == []:
#         return []

#     avg_buy_volume = exchange.buy_orders[0].amount

#     for order in exchange.buy_orders:
#         if order.amount > SANAL * avg_buy_volume:
#             return [Order("buy", order.price + 1, )]