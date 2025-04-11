import pandas as pd
from strategy import SmaCrossStrategy
from broker import Broker

class Backtest:
    def __init__(self, data, strategy_class):
        self.data = data
        self.broker = Broker()
        self.strategy = strategy_class(data, self.broker)

    def run(self):
        for i in range(len(self.data)):
            self.strategy.on_data(i)
        final_price = self.data.iloc[-1]['close']
        print("Final Equity:", self.broker.equity(final_price))
