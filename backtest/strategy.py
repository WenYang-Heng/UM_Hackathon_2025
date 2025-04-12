import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data):
        self.data = data
        self.backtest_result = []

    def record(self, date, price, price_change, position, trade, pnl, equity, drawdown):
        self.backtest_result.append({
            'date': date,
            'price': price,
            'price_change': price_change,
            'position': position,
            'trade': trade,
            'pnl': pnl,
            'equity': equity,
            'drawdown': drawdown
        })

    def process(self, i):
        pass

class SmaCrossStrategy(Strategy):
    def __init__(self, data, window, initial_cash=10000):
        super().__init__(data)
        self.data = data.reset_index(drop=True)
        self.window = window
        self.initial_cash = initial_cash

        self.cash = initial_cash
        self.btc = 0
        self.history = []
        self.prev_signal = 0
        self.cumulative_pnl = 0

    def process(self, i):
        row = self.data.iloc[i]
        price = row['close']
        date = row['date']
        trade_actions = 0
        fee_rate = 0.0006

        # Calculate price change
        # (current row close price/ previous row close price) - 1 or (current row close price - previous row close price) / previous row
        # if it is the first row, price change is 0
        if i > 0:
            prev_price = self.data.iloc[i - 1]['close']
            price_change = (price - prev_price) / prev_price
        else:
            prev_price = price
            price_change = 0

        # Generate signal
        signal = self.prev_signal
        if i >= self.window:
            sma = self.data['close'].iloc[i - self.window:i].mean()
            if price > sma:
                signal = 1
            elif price < sma:
                signal = -1
            else:
                signal = 0

        # Trade actions
        if signal != self.prev_signal:
            if abs(signal - self.prev_signal) == 2:
                trade_actions = 2
            else:
                trade_actions = 1

        # Calculate PnL
        # (price change * previous position) - (number of trade action for current row * fees)
        pnl = price_change * self.prev_signal
        fees = trade_actions * fee_rate
        pnl -= fees

        # Equity
        self.cumulative_pnl += pnl

        # MDD
        # current equity - max of all previous equity
        if len(self.backtest_result) > 0:
            max_equity = max(h['equity'] for h in self.backtest_result)
        else:
            max_equity = self.cumulative_pnl

        drawdown = self.cumulative_pnl - max_equity        
        self.record(date, price, price_change, signal, trade_actions, pnl, self.cumulative_pnl, drawdown)
        self.prev_signal = signal

    # def final_equity(self):
    #     return self.backtest_result[-1]['equity'] if self.backtest_result else self.initial_cash

    def results(self):
        return pd.DataFrame(self.backtest_result)