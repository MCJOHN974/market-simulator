import datetime
from trader import Trader

class Order:
    def __init__(self, order_type: str, price: int, amount: int, trader: Trader, order_id: int, date=None):
        self.order_type = order_type
        self.price = price
        self.amount = amount
        self.date = date if date else datetime.datetime.now()
        self.trader = trader
        self.order_id = order_id


    def __lt__(self, other):
        return [self.price, self.order_id] < [other.price, other.order_id]
