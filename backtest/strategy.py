import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data):
        self.data = data

    def on_data(self, i):
        pass

class SmaCrossStrategy:
    def __init__(self, data, window, initial_cash=10000):
        self.data = data.reset_index(drop=True)
        self.window = window
        self.initial_cash = initial_cash

        self.cash = initial_cash
        self.btc = 0
        self.history = []
        self.prev_signal = 0
        self.cumulative_pnl = 0

    def on_data(self, i):
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
        if len(self.history) > 0:
            max_equity_so_far = max(h['equity'] for h in self.history)
        else:
            max_equity_so_far = self.cumulative_pnl  # first value

        drawdown = self.cumulative_pnl - max_equity_so_far

        # Execute Trades
        # if trade_actions > 0:
        #     # Exit any previous position
        #     if self.prev_signal == 1:
        #         self.cash = self.btc * price
        #         self.btc = 0
        #     elif self.prev_signal == -1:
        #         self.cash = self.cash - self.btc * price  # buy back short
        #         self.btc = 0

        #     # Enter new position
        #     if signal == 1:
        #         self.btc = self.cash / price
        #         self.cash = 0
        #     elif signal == -1:
        #         self.btc = -self.cash / price  # simulate borrowing and selling BTC
        #         self.cash = self.cash * 2      # receive cash from shorting

        self.history.append({
            'date': date,
            'price': price,
            'price_change': price_change,
            'position': signal,
            'trade': trade_actions,
            'pnl': pnl,
            'equity': self.cumulative_pnl,
            'drawdown': drawdown
        })

        self.prev_signal = signal

    def final_equity(self):
        return self.history[-1]['equity'] if self.history else self.initial_cash

    def results(self):
        return pd.DataFrame(self.history)