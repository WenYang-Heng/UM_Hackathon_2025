import pandas as pd
from .strategy import SmaCrossStrategy

class Backtest:
    def __init__(self, data, strategy_class, **strategy_kwargs):
        self.data = data
        self.strategy = strategy_class(data, **strategy_kwargs)

    def run(self):
        for i in range(len(self.data)):
            self.strategy.on_data(i)
        return self.strategy.results()
