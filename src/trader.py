class Trader:
    def __init__(self, exchange, strategy) -> None:
        self.usd = 0
        self.jcoin = 0
        self.exchange = exchange
        self.strategy = strategy


    def deposit_usd(self, amount: int) -> None:
        self.usd += amount


    def deposit_jcoin(self, amount: int) -> None:
        self.jcoin += amount


    def generate_orders(self):
        orders = self.strategy(self)
        for order in orders:
            self.exchange.place_order(order)
