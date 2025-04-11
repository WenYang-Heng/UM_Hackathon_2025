class Strategy:
    def __init__(self, data, broker):
        self.data = data
        self.broker = broker

    def on_data(self, i):
        # Placeholder: override in subclass
        pass

class SmaCrossStrategy(Strategy):
    def on_data(self, i):
        if i < 20: return  # not enough data
        window = self.data.iloc[i-20:i]
        ma = window['close'].mean()
        price = self.data.iloc[i]['close']

        if price > ma:
            self.broker.buy('BTC', 1, price)
        else:
            self.broker.sell('BTC', 1, price)
