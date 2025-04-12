import pandas as pd
import numpy as np
from .utils import (
    calculate_drawdown,
    calculate_price_change,
    calculate_trade_actions,
    calculate_pnl
)

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
        price_change = calculate_price_change(i, self.data)

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
        trade_actions = calculate_trade_actions(self.prev_signal, signal)

        # Calculate PnL
        # (price change * previous position) - (number of trade action for current row * fees)
        pnl = calculate_pnl(price_change, self.prev_signal, trade_actions, fee_rate)

        # Equity
        self.cumulative_pnl += pnl

        # MDD
        drawdown = calculate_drawdown(self.cumulative_pnl, self.backtest_result)       
        self.record(date, price, price_change, signal, trade_actions, pnl, self.cumulative_pnl, drawdown)
        self.prev_signal = signal

    # def final_equity(self):
    #     return self.backtest_result[-1]['equity'] if self.backtest_result else self.initial_cash

    def results(self):
        return pd.DataFrame(self.backtest_result)
    
class ExchangeFlowStrategy(Strategy):
    def __init__(self, data, initial_cash=10000, threshold=1000):
        super().__init__(data)
        self.data = data.reset_index(drop=True)
        self.initial_cash = initial_cash
        self.threshold = threshold

        self.cash = initial_cash
        self.btc = 0
        self.history = []
        self.prev_signal = 0
        self.cumulative_pnl = 0

    def process(self, i):
        row = self.data.iloc[i]
        date = row['date']
        price = row['close']
        inflow = row['inflow_total']
        outflow = row['outflow_total']

        net_flow = inflow - outflow
        fee_rate = 0.0006
        trade_actions = 0

        # Generate signal
        if net_flow > self.threshold:
            signal = -1  # Sell
        elif net_flow < -self.threshold:
            signal = 1   # Buy
        else:
            signal = 0   # Hold

        # Trade actions
        trade_actions = calculate_trade_actions(self.prev_signal, signal)

        # PnL calculation
        if i > 0:
            prev_price = self.data.iloc[i - 1]['close']
            price_change = (price - prev_price) / prev_price
        else:
            price_change = 0

        pnl = calculate_pnl(price_change, self.prev_signal, trade_actions, fee_rate)

        self.cumulative_pnl += pnl

        # Drawdown
        drawdown = calculate_drawdown(self.cumulative_pnl, self.history)  

        self.history.append({
            'date': date,
            'price': price,
            'position': signal,
            'net_flow': net_flow,
            'trade': trade_actions,
            'pnl': pnl,
            'equity': self.cumulative_pnl,
            'drawdown': drawdown
        })

        self.prev_signal = signal

    def run(self):
        for i in range(len(self.data)):
            self.process(i)
        return pd.DataFrame(self.history)