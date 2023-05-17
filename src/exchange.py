from order import Order
from trader import Trader



# amount everywhere is amount of jcoins


class Exchange:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.__trades__ = []
    

    def match_orders(self):
        print("match orders")
        while len(self.buy_orders) > 0 and len(self.sell_orders) > 0 and self.buy_orders[-1].price >= self.sell_orders[0].price:
            print("iteration")
            self.make_trade(self.buy_orders[0], self.sell_orders[-1])

    def make_trade(self, buy: Order, sell: Order):
        print("make trade")
        self.__trades__.append({"buy_price": buy.price, "sell_price": sell.price, "buy_amount": buy.amount, "sell_amount": sell.amount})
        if buy.amount > sell.amount:
            # selling all
            sell.trader.usd += sell.amount * sell.price
            buy.trader.jcoin += sell.amount
            buy.amount -= sell.amount
            self.sell_orders.remove(sell)
        elif buy.amount < sell.amount:
            buy.trader.jcoin += buy.amount
            sell.trader.usd += buy.amount * sell.price
            sell.amount -= buy.amount
            self.buy_orders.remove(buy)
        else:
            buy.trader.jcoin += buy.amount
            sell.trader.usd += sell.amount * sell.price
            self.sell_orders.remove(sell)
            self.buy_orders.remove(buy)


    def orderbook(self):
        return {'buy_orders': self.buy_orders, 'sell_orders': self.sell_orders}

    def trades(self):
        return self.__trades__[-50:] if len(self.__trades__) > 50 else self.__trades__

    def place_order(self, order: Order):
        if order.order_type == "buy":
            if order.trader.usd <= order.amount * order.price:
                return

            order.trader.usd -= order.amount * order.price
            self.buy_orders.append(order)
            self.buy_orders.sort()
        elif order.order_type == "sell":
            if order.trader.jcoin <= order.amount:
                return

            order.trader.jcoin -= order.amount
            self.sell_orders.append(order)
            self.sell_orders.sort()
        else:
            raise Exception(f"Invalid order type. order_type = {order.order_type}")
